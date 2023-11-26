import os
import time
import pika
import sys
from services.database import store_message

def subscribe(SERVER_ID, DB_PATH):

    print("Starting subscribing")
    connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='rabbitMQ'))
    channel = connection.channel()

    channel.exchange_declare(exchange='ds_messages', exchange_type='fanout')

    result = channel.queue_declare('', exclusive=True)
    queue_name = result.method.queue

    binding_keys = ["messages"]

    for binding_key in binding_keys:
        channel.queue_bind(
            exchange='ds_messages', queue=queue_name, routing_key=binding_key)

    print(' [*] Waiting for logs. To exit press CTRL+C')




    def callback(ch, method, properties, body):
       
        store_message({ "msg": f"{body}", "db_path": DB_PATH })


    channel.basic_consume(
        queue=queue_name,
        on_message_callback=callback,
        auto_ack=True)

    channel.start_consuming()

