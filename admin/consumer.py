import pika

params = pika.URLParameters('amqps://lvtbhjno:KO5sOzrpJntPFAUtJlAag49ksPGo20KX@moose.rmq.cloudamqp.com/lvtbhjno')

connection = pika.BlockingConnection(params)

channel = connection.channel()

channel.queue_declare(queue='admin')


def callback(ch, method, properties, body):
    print('Received in admin')
    print(body)


channel.basic_consume(queue='admin', on_message_callback=callback, auto_ack=True)

print('Started consuming')

channel.start_consuming()

channel.close()
