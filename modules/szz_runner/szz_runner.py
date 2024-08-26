#!/usr/bin/env python
import pika
import yaml
import psycopg2
import psycopg2.extras

import json
import functools
import threading

from szz_selector import run as run_szz


with open('config/config.yml', 'r') as file:
    config = yaml.safe_load(file)

datasource = config['datasource']

def get_connection():
    conn = psycopg2.connect(user=datasource['username'],
                    password=datasource['password'],
                    host=datasource['host'],
                    port=datasource['port'],
                    dbname=datasource['database'])
    
    return conn

def insert_szz_result(repo_url: str, bugfix_commit_hash: str, bug_commit_hashes: list, szz_variant: str):
    query = f"""INSERT INTO bug_to_fix (repository_url, szz_variant, bugfix_commit_hash, bug_commit_hashes) values (%s, %s, %s, %s);"""
    conn = get_connection()
    cur = conn.cursor(cursor_factory = psycopg2.extras.DictCursor)

    cur.execute(query, (repo_url, szz_variant, bugfix_commit_hash, bug_commit_hashes))

    conn.commit()
    cur.close()
    conn.close()

def complete_request(request_id: int, fix_commit_hash: str):
    query = f"""UPDATE request_status SET finished = TRUE WHERE request_id = {request_id} AND bugfix_commit_hash = '{fix_commit_hash}';"""
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(query)

    conn.commit()
    cur.close()
    conn.close()

def ack_message(ch, delivery_tag):
    if ch.is_open:
        ch.basic_ack(delivery_tag)
    else:
        print('Channel closed!')


def do_work(ch, delivery_tag, body):
    thread_id = threading.get_ident()
    print('Thread id: {} Delivery tag: {} Message body: {}'.format(thread_id, delivery_tag, body))

    request = json.loads(body.decode())
    szz_variant = request['szz_variant']
    szz_name = szz_variant.split('_')[0].lower()
    repo_url = request['repository_url']
    fix_commit_hash = request['bugfix_commit_hash']

    result = run_szz(szz_name=szz_name, fix_commit_hash=fix_commit_hash, repo_url=repo_url, repos_dir=None)
    complete_request(request_id=request['request_id'], fix_commit_hash=fix_commit_hash)
    
    print(f" {result}")
    insert_szz_result(repo_url=repo_url, bugfix_commit_hash=fix_commit_hash, bug_commit_hashes=result, szz_variant=szz_variant)
    print(" [x] Done")
    cb = functools.partial(ack_message, ch, delivery_tag)
    ch.connection.add_callback_threadsafe(cb)


def on_message(ch, method_frame, _header_frame, body, args):
    thrds = args
    delivery_tag = method_frame.delivery_tag
    t = threading.Thread(target=do_work, args=(ch, delivery_tag, body))
    t.start()
    thrds.append(t)


# Note: sending a short heartbeat to prove that heartbeats are still
# sent even though the worker simulates long-running work
def main():
    print(' [*] Waiting for messages. To exit press CTRL+C')
    parameters = pika.ConnectionParameters(config['rabbitmq']['host'])
    connection = pika.BlockingConnection(parameters)

    channel = connection.channel()
    channel.queue_declare(queue="szz_request", durable=True)
    # Note: prefetch is set to 1 here as an example only and to keep the number of threads created
    # to a reasonable amount. In production you will want to test with different prefetch values
    # to find which one provides the best performance and usability for your solution
    channel.basic_qos(prefetch_count=1)

    thread_pool = []
    on_message_callback = functools.partial(on_message, args=thread_pool)
    channel.basic_consume(on_message_callback=on_message_callback, queue='szz_request')

    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        channel.stop_consuming()

    # Wait for all to complete
    for thread in thread_pool:
        thread.join()

    connection.close()
    print('FINISHING')

if __name__ == '__main__':
    main()