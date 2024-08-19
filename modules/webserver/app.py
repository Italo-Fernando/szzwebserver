from queries import *
from flask import Flask, request, jsonify
from classes.response import ApiResponse
import pika
import threading
import json
import logging

logger = logging.getLogger(__name__)
app = Flask(__name__)


@app.get('/szz/variants')
def szz_variants():
    result = get_szz_variants()
    response = [{'variant_name': row['variant_name']} for row in result]
    return response

@app.get('/szz/bug_commits/<request_id>')
def check_result(request_id):
    request_data = get_request_data(request_id=request_id)
    finished_count = check_request_finished(request_id=request_id)
    response = ApiResponse(szz_variant=request_data['szz_variant'])

    if finished_count == request_data['commit_count']:
        response.status = 'FINISHED'
        result = find_processed_bugfix_commits(repo_url=request_data['repository_url'], 
                                           fix_commit_list=request_data['bugfix_commit_hashes'], 
                                           szz_variant=request_data['szz_variant'])
        for row in result:
            bug_to_fix = { 'fix_commit_hash' : row['bugfix_commit_hash'], 'bug_commit_hash' : []}
            for bug_commit_hash in row['bug_commit_hashes']:
                bug_to_fix['bug_commit_hash'].append(bug_commit_hash)

            response.result.append(bug_to_fix)
    else:
        response.status = 'PROCESSING' if finished_count > 0 else 'WAITING'
    
    return jsonify(response)

@app.post('/szz/fix_commits')
def find_bug_commits():

    # TODO: Validate input
    # TODO: Validate non-empty bugfix_commit_hash set
    # TODO: Validate commit hashes
    requested_commit_list = list(set(commit_hash for commit_hash in request.json['fix_commit_hash']))
    szz_variant = request.json['szz_variant']
    repo_url = request.json['repository_url']

    request_id = insert_request(repo_url=repo_url, szz_variant=szz_variant, fix_commit_list=requested_commit_list)

    result = find_processed_bugfix_commits(repo_url=repo_url, 
                                           fix_commit_list=requested_commit_list, 
                                           szz_variant=szz_variant)
    
    retrieved_commit_list = [row['bugfix_commit_hash'] for row in result]
    for commit_hash in requested_commit_list:
        if commit_hash in retrieved_commit_list:
            print(f"Already processed commit[{commit_hash}]. No work is needed.")
            insert_request_status(request_id=request_id, bugfix_commit_hash=commit_hash, finished=True)
        else:
            # TODO: Send to rabbitmq queue and
            message = {'request_id' : request_id, 'repository_url':repo_url, 'bugfix_commit_hash':commit_hash, 'szz_variant': szz_variant}
            insert_request_status(request_id=request_id, bugfix_commit_hash=commit_hash, finished=False)
            connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
            channel = connection.channel()
            channel.queue_declare(queue='szz_request', durable=True)
            channel.basic_publish(exchange='', 
                                  routing_key='szz_request', 
                                  body=json.dumps(message), 
                                  properties=pika.BasicProperties(content_type='application/json', delivery_mode=pika.DeliveryMode.Persistent))
            channel.close()
            connection.close()

    return {'request_id' : request_id}

def main():
    global connection, channel
    connection = pika.BlockingConnection(pika.ConnectionParameters(config['rabbitmq']['host']))
    channel = connection.channel()
    channel.queue_declare(queue='szz_request', durable=True)
    t = threading.Thread(target=app.run)
    t.start()
    t.join()


if __name__ == '__main__':
   main()