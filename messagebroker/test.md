

## how to

### Listen to a topic:

    curl -d '{ "ip": "localhost", "port": 7777, "path": "message", "topic": "msgs" }' localhost:3000/listen

### Send a message to a topic: 

    curl -d '{ "message": "HAHAHA", "topic": "msgs" }' localhost:3000/message


##  What will happen? 

The messagebroker (running in 3000) will add localhost:7777 as a listener under the topic "msgs".

When the msgbroker receives a message under topic "msgs", it will iterate through all listeners under said topic, 
and post a request to them (to the port & path described when declaring a listener).

# TODO

deploy dummy gameserver and messagebroker to HY-machines. Show proof of concept via communication