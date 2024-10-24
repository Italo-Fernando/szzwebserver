#!/usr/bin/env python
import pika
import yaml
import psycopg2
import psycopg2.extras
import logging as log
import time
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

def check_execution(repo_url: str, fix_commit_hash: str, szz_variant: str):
    query = f"""SELECT TRUE FROM execution_result 
                WHERE repository_url = (%s) AND szz_variant = (%s) AND bugfix_commit_hash = (%s);"""
    conn = get_connection()
    cur = conn.cursor(cursor_factory = psycopg2.extras.DictCursor)

    cur.execute(query, (repo_url, szz_variant, fix_commit_hash))
    result = cur.fetchone()

    conn.commit()
    cur.close()
    conn.close()
    
    return result

def check_all_links_finished(request_id):
    query = f"""SELECT TRUE FROM commit_to_request_link 
                WHERE request_id = %s AND request_status != 'FINISHED'"""
    conn = get_connection()
    cur = conn.cursor(cursor_factory = psycopg2.extras.DictCursor)

    cur.execute(query, (request_id,))
    result = cur.fetchone()

    conn.commit()
    cur.close()
    conn.close()

    return (result is None) 

def insert_szz_result(repo_url: str, bugfix_commit_hash: str, bug_commit_hashes: list, szz_variant: str):
    query = f"""INSERT INTO execution_result (repository_url, szz_variant, bugfix_commit_hash, bug_commit_hashes) values (%s, %s, %s, %s);"""
    conn = get_connection()
    cur = conn.cursor(cursor_factory = psycopg2.extras.DictCursor)

    cur.execute(query, (repo_url, szz_variant, bugfix_commit_hash, bug_commit_hashes))

    conn.commit()
    cur.close()
    conn.close()

def update_link(request_id: int, fix_commit_hash: str, repository_url: str, szz_variant: str, new_status: str):
    query = f"""UPDATE commit_to_request_link SET request_status = (%s)
                WHERE request_id = %s AND bugfix_commit_hash = (%s) AND repository_url = (%s) AND szz_variant = (%s);"""
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(query, (new_status, request_id, fix_commit_hash, repository_url, szz_variant))

    conn.commit()
    cur.close()
    conn.close()


def update_request(request_id: int, new_status: str):
    query = f"""UPDATE request SET request_status = (%s)
                WHERE request_id = %s;"""
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(query, (new_status, request_id))

    conn.commit()
    cur.close()
    conn.close()

def ack_message(ch, delivery_tag):
    if ch.is_open:
        ch.basic_ack(delivery_tag)
    else:
        log.info('Channel closed!')


def do_work(ch, delivery_tag, body):
    thread_id = threading.get_ident()
    start_work = time.time()
    log.info('Thread id: {} Delivery tag: {} Message body: {}'.format(thread_id, delivery_tag, body))

    request = json.loads(body.decode())
    szz_variant = request['szz_variant']
    szz_name = szz_variant.split('_')[0].lower()
    repo_url = request['repository_url']
    fix_commit_hash = request['bugfix_commit_hash']

    result = check_execution(repo_url=repo_url, fix_commit_hash=fix_commit_hash, szz_variant=szz_variant) 
    if result is None:
        update_link(new_status='PROCESSING', request_id=request['request_id'], fix_commit_hash=fix_commit_hash, szz_variant=szz_variant, repository_url=repo_url)
        bug_commits = run_szz(szz_name=szz_name, fix_commit_hash=fix_commit_hash, repo_url=repo_url, repos_dir=None)
    
        log.info(f"result: {bug_commits}")
        insert_szz_result(repo_url=repo_url, bugfix_commit_hash=fix_commit_hash, bug_commit_hashes=bug_commits, szz_variant=szz_variant)
    else:
        log.info(f"Combination {repo_url, fix_commit_hash, szz_variant} already processed")

    log.info("------------------")
    update_link(new_status='FINISHED', request_id=request['request_id'], fix_commit_hash=fix_commit_hash, szz_variant=szz_variant, repository_url=repo_url)

    if check_all_links_finished(request_id=request['request_id']):
        update_request(new_status='FINISHED', request_id=request['request_id'])
        


    log.info(" [x] Done")
    end_work = time.time()
    elapsed_time = end_work - start_work
    timestamp = int(end_work * 1000000)
    with open(f'/measures/total_{timestamp}.txt', 'w+') as file:
        file.write(f"{elapsed_time}")

    cb = functools.partial(ack_message, ch, delivery_tag)
    ch.connection.add_callback_threadsafe(cb)


def on_message(ch, method_frame, _header_frame, body, thread_pool):
    thrds = thread_pool
    delivery_tag = method_frame.delivery_tag
    t = threading.Thread(target=do_work, args=(ch, delivery_tag, body))
    t.start()
    thrds.append(t)


# Note: sending a short heartbeat to prove that heartbeats are still
# sent even though the worker simulates long-running work
def main():
    log.info(' [*] Waiting for messages. To exit press CTRL+C')
    parameters = pika.ConnectionParameters(host=config['rabbitmq']['host'], port=config['rabbitmq']['port'])
    connection = pika.BlockingConnection(parameters)

    channel = connection.channel()
    channel.queue_declare(queue="szz_request", durable=True)
    # Note: prefetch is set to 1 here as an example only and to keep the number of threads created
    # to a reasonable amount. In production you will want to test with different prefetch values
    # to find which one provides the best performance and usability for your solution
    channel.basic_qos(prefetch_count=1)

    thread_pool = []
    on_message_callback = functools.partial(on_message, thread_pool=thread_pool)
    channel.basic_consume(on_message_callback=on_message_callback, queue='szz_request')

    log.info("Start consuming!")
    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        channel.stop_consuming()

    # Wait for all to complete
    for thread in thread_pool:
        thread.join()

    connection.close()
    log.info('FINISHING')

if __name__ == '__main__':
    main()

