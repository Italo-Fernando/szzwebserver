from queries import *
from flask import Flask, request, jsonify, Response
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

    if request_data is None:
        return Response('Request not found.', status=404)
    
    finished_count = get_request_finished_count(request_id=request_id)
    response = ApiResponse(szz_variant=request_data['szz_variant'])

    if finished_count == len(request_data['bugfix_commit_hashes']):
        response.status = 'FINISHED'
        result = find_processed_bugfix_commits(repo_url=request_data['repository_url'], 
                                           fix_commit_list=request_data['bugfix_commit_hashes'], 
                                           szz_variant=request_data['szz_variant'])
        for row in result:
            execution_result = { 'fix_commit_hash' : row['bugfix_commit_hash'], 'bug_commit_hash' : []}
            for bug_commit_hash in row['bug_commit_hashes']:
                execution_result['bug_commit_hash'].append(bug_commit_hash)

            response.result.append(execution_result)
    else:
        response.status = 'PROCESSING' if finished_count > 0 else 'WAITING'
    
    return jsonify(response)

@app.post('/szz/fix_commits')
def find_bug_commits():

    # TODO: Validate input
    requested_commit_list = list(set(commit_hash for commit_hash in request.json['fix_commit_hash']))

    if len(requested_commit_list) == 0:
        return Response("Bugfix commit list cannot be empty", status=400)
    
    szz_variant = request.json['szz_variant']
    repo_url = request.json['repository_url']

    request_id = insert_request(repo_url=repo_url, szz_variant=szz_variant, fix_commit_list=requested_commit_list)

    result = find_processed_bugfix_commits(repo_url=repo_url, 
                                           fix_commit_list=requested_commit_list, 
                                           szz_variant=szz_variant)
    
    retrieved_commit_list = [row['bugfix_commit_hash'] for row in result]
    for commit_hash in requested_commit_list:
        if commit_hash in retrieved_commit_list:
            app.logger.info("Already processed commit[%s]. No work is needed.", commit_hash)
            insert_link(status='FINISHED', request_id=request_id, bugfix_commit_hash=commit_hash, repository_url=repo_url, szz_variant=szz_variant)
        else:
            message = {'request_id' : request_id, 'repository_url':repo_url, 'bugfix_commit_hash':commit_hash, 'szz_variant': szz_variant}
            insert_link(status='WAITING', request_id=request_id, bugfix_commit_hash=commit_hash, repository_url=repo_url, szz_variant=szz_variant)
            
            connection = pika.BlockingConnection(pika.ConnectionParameters(config['rabbitmq']['host']))
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
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=config['rabbitmq']['host']), port=config['rabbitmq']['port'])
    channel = connection.channel()
    channel.queue_declare(queue='szz_request', durable=True)
    t = threading.Thread(target=app.run)
    t.start()
    t.join()


if __name__ == '__main__':
   main()