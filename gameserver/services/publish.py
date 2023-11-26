import pika


def publish(message="Hello world"):
    print(f"Publishin' message {message}")

    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='rabbitMQ'))
    channel = connection.channel()

    channel.exchange_declare(exchange='ds_messages', exchange_type='fanout')

    routing_key = "messages"
    
    channel.basic_publish(
        exchange='ds_messages',
        routing_key=routing_key,
        body=message
    )
    print(f" [x] Sent {routing_key}:{message}")
    connection.close()