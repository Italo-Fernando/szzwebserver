#!/usr/bin/env python
import pika
import time
import json
from queries import complete_request
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='szz_request', durable=True)

print(' [*] Waiting for messages. To exit press CTRL+C')


def callback(ch, method, properties, body):
    request = json.loads(body.decode())
    print(f" [x] Received {body.decode()}")
    complete_request(request_id=request['request_id'], bugfix_commit_hash=request[' bugfix_commit_hash'])
    ch.basic_ack(delivery_tag=method.delivery_tag)
    print(" [x] Done")


channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='szz_request', on_message_callback=callback)

channel.start_consuming()