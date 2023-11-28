import pika


def publish(exchange, message="Hello world"):

    print(f"Publishin' message {message} to exchange {exchange}")

    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='rabbitMQ'))
    channel = connection.channel()

    channel.exchange_declare(exchange=exchange, exchange_type='fanout')

    
    channel.basic_publish(
        exchange=exchange,
        routing_key='',
        body=message
    )
    print(f" [x] Sent {exchange}:{message}")
    connection.close()