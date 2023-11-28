import pika

def subscribe(exchange, callback):

    print("Starting subscribing")
    connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='rabbitMQ'))
    channel = connection.channel()

    channel.exchange_declare(exchange=exchange, exchange_type='fanout')

    # Luo väliaikaisen jonon, joka elää vain kuuntelun ajan (exclusive=True)
    result = channel.queue_declare('', exclusive=True)
    queue_name = result.method.queue

    # Liitetään jono "vaihteeseen"
    channel.queue_bind(exchange=exchange, queue=queue_name)

    print(' [*] Waiting for logs. To exit press CTRL+C')

    channel.basic_consume(
        queue=queue_name,
        on_message_callback=callback,
        auto_ack=True)

    channel.start_consuming()

