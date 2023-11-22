import pika, sys, os

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='server-queue')

def callback(ch, method, properties, body):
    print(f" [x] Received {body}")

channel.basic_consume(queue='server-queue', on_message_callback=callback, auto_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()