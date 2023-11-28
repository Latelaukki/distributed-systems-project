# distributed-systems-project

## Frontend

Frontend is built with Tkinter but can be changed to PyGame.

Frontend can be started by running the main.py file in [src/](/src) folder:

```
python3 main.py
```
Responses is printed in the terminal.

The frontend displays the number of the maze in which the player is atm.

## Backend
- Uses Python FastApi and Uvicorn to create servers
- Uses RabbitMQ for message queues
- Docker for running the services

How to run with Docker. Use with `--build` flag if you're running the app for the first time.

1. Start by setting up the message-broker in one terminal with `cd rabbitmq && docker compose up`.
2. When rabbitmq is up, open another terminal and do `cd gameserver && docker compose up`. This will start three fast-api's and a nginx-reverse proxy.

Then you access the api in [http://localhost:7800](http://localhost:7800)

## Architecture atm


At the moment the project is as follows

 ![Architecture](/documentation/architecture.png)


When a player clicks a button to enter, for example, maze 1, a request is passed via the reverse proxy to one of the servers. The server then publishes the request to the message broker from which it is passed onto all of the servers (itself also?). 

The servers all subscribe to the same message topic. When they receive a message they store it to a local sqlite-database. You can see a list of stored messages of a (random) server from [http://localhost:7800/messages](http://localhost:7800/messages).

For example this shows thatserver with ID *89f709..* has stored two messages. One originating from itself and one from *5042898c ..*. Each server is assigned an uuid when started.

 ![messages-example](/documentation/messages-example.png)


## Notes

- `gameserver/services/publish.py` and `gameserver/services/subscribe.py` are pretty much copied from: [RabbitMQ Publish/Subscribe](https://www.rabbitmq.com/tutorials/tutorial-three-python.html) 

- nginx acts as a load balancer. Each request to port 7800 is passed one of the three gameservers (dont which one up ahead). It does not know anything about the contents of the requests.
- All messages are posted under the same topic (the pub/sub functions should accept the topic as a parameter)
