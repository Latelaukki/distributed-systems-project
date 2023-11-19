# distributed-systems-project

## Frontend

Frontend is built with Tkinter but can be changed to PyGame.

Frontend can be started by running the main.py file in [src/](/src) folder:

```
python3 main.py
```
Responses is printed in the terminal.

## Backend
- Uses Python FastApi and Uvicorn to create servers
- Uses RabbitMQ for message queues
- Docker for running the services

How to run with Docker:

Navigate to [src/backend](/src/backend) folder and use Docker compose to start services:
```
cd /src/backend
sudo docker compose up --build
```

Ports to access the services through web broswer can be found in the compose.yaml file PORTS variable, e.g:
``` 
  fast-api-server:
    build: 
      context: .
      dockerfile: fast-api.Dockerfile
    volumes:
      - ./:/src
    ports:
      - '81-83:80'
    deploy:
      replicas: 3
```
Servers can be accessed through web browser e.g http://localhost:81/

### RabbitMQ:
[src/backend/rabbitmq](src/backend/rabbitmq) folder contains a basic template for using RabbitMQ. 

Currently the RabbitMQ container does not communicate with the servers or the frontend.

RabbitMQ management service UI is accessable through http://localhost:15672/ with credentials:

```
username: guest
```
```
password: guest 
```

Messages can be send and received with by running send.py and receive.py files in [src/backend/rabbitmq](src/backend/rabbitmq)


Sending and receiving needs the Pika package, install it with python virtual environment enabled:

```
pip install pika
```
```
python3 send.py
```
After running send.py, queues can be monitored through the RabbitMQ management service on http://localhost:15672

To consume messages from RabbitMQ run:
```
python3 receive.py
```
Message from the queue will be printed in the terminal
