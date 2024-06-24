from setup import app, channel, connection
from queries import *
from flask import request, jsonify, abort
import uuid, pika
import threading
import json

@app.get('/szz/variants')
def szz_variants():
    result = get_szz_variants()
    response = [{'variant_name': row['variant_name']} for row in result]
    return response

@app.get('/szz/bug_commits/<request_id>')
def check_result(request_id):
    request_data = get_request_data(request_id=request_id)
    finished_count = check_request_finished(request_id=request_id)
    
    if finished_count == len(request_data['bugfix_commit_hashes']):
        result = find_processed_bugfix_commits(repo_url=request_data['repository_url'], 
                                           bugfix_list=request_data['bugfix_commit_hashes'], 
                                           szz_variant=request_data['szz_variant'])
        return {
                'szz_variant': request_data['szz_variant'],
                'status' : 'FINISHED',
                'result' : [
                                { 
                                    'bugfix_commit_hash' :row['bugfix_commit_hash'],
                                    'bug_commit_hash' : [bug_commit_hash for bug_commit_hash in row['bug_commit_hashes']]
                                } for row in result ] 
                }
    else:
        return {'szz_variant': request_data['szz_variant'], 
                'status' : 'PROCESSING' if finished_count > 0 else 'WAITING',
                'result' : []}

@app.post('/szz/find_bug_commits/')
def find_bug_commits():

    # TODO: Validate input
    # TODO: Validate non-empty bugfix_commit_hash set
    # TODO: Validate commit hashes
    requested_commit_list = [commit_hash for commit_hash in request.json['bugfix_commit_hash']]
    szz_variant = request.json['szz_variant']
    repo_url = request.json['repository_url']

    request_id = insert_request(repo_url=repo_url, szz_variant=szz_variant, bugfix_list=requested_commit_list)

    result = find_processed_bugfix_commits(repo_url=repo_url, 
                                           bugfix_list=requested_commit_list, 
                                           szz_variant=szz_variant)
    
    retrieved_commit_list = [row['bugfix_commit_hash'] for row in result]
    for commit_hash in requested_commit_list:
        if commit_hash in retrieved_commit_list:
            # TODO: Add constraint in DB to not accept duplicates of (request_id, commit_hash)
            insert_request_status(request_id=request_id, bugfix_commit_hash=commit_hash, finished=True)
        else:
            # TODO: Send to rabbitmq queue and
            message = {'request_id' : request_id, 'repository_url':repo_url, 'bugifx_commit_hash':commit_hash, 'szz_variant': szz_variant}
            insert_request_status(request_id=request_id, bugfix_commit_hash=commit_hash, finished=False)
            channel.basic_publish(exchange='', 
                                  routing_key='szz_request', 
                                  body=json.dumps(message), 
                                  properties=pika.BasicProperties(content_type='application/json', delivery_mode=pika.DeliveryMode.Persistent))


    return {'request_id' : request_id}

if __name__ == '__main__':
    # TODO: When initializing look for unprocessed request and publish to rabbitmq queues
    t = threading.Thread(target=app.run)
    t.start()
    t.join()
    connection.close()
