import json

import pika

params = pika.URLParameters('amqps://lvtbhjno:KO5sOzrpJntPFAUtJlAag49ksPGo20KX@moose.rmq.cloudamqp.com/lvtbhjno')


def publish(method, body):
    properties = pika.BasicProperties(method)

    connection = pika.BlockingConnection(params)

    channel = connection.channel()
    channel.basic_publish(exchange='', routing_key='main', body=json.dumps(body), properties=properties)
    connection.close()

