from flask import Flask
import yaml
from flask_sqlalchemy import SQLAlchemy
import uuid
from sqlalchemy.dialects.postgresql import UUID
from dataclasses import dataclass
import pika

# TODO: Pass config file path as arguments to the program 
with open('config/config.yml', 'r') as file:
    config = yaml.safe_load(file)


datasource = config['datasource']

app = Flask(__name__)

# postgresql_uri = f"postgresql://{datasource['username']}:{datasource['password']}@{datasource['host']}:{datasource['port']}/{datasource['database']}"

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='szz_request', durable=True)
