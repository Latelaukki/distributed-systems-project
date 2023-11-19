import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='server-queue')

channel.basic_publish(exchange='',
                      routing_key='server-queue',
                      body='this is the message')
print("Message sent to rabbitMQ")
connection.close()
