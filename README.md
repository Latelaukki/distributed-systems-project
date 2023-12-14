# distributed-systems-project

The application consist of

- Gameservers responsible for handling events in the game
- Load balancer that allocates clients to servers
- Messagebroker that passes messages between servers
- A frontend for interacting with the system

These are further explained in the project final report.

## Frontend

Frontend is built with Tkinter but can be changed to PyGame.

Frontend can be started by running the main.py file in [src/](/src) folder:
```
python3 main.py
```
Responses are printed in the terminal.

## Deploying the project onto HY-machines

Setup SSH-connections and copy files using this guide:

    https://helpdesk.it.helsinki.fi/en/instructions/logging-and-connections/using-cubbli-workstation-home-computer#using-cubbli-on-a-linux-home-computer

Specically follow guidelines from `If you also need to copy files between your home ...` onwards.

After configuration, do something like this (assuming you named the machines duuni1, duuni2, etc..)

    ssh -f -N -q pangtunnel 
    scp -r gameserver/*.* duuni1:
    scp -r gameserver/services duuni1:
    scp -r messagebroker/ duuni1:
    scp -r loadbalancer/ duuni1:

You should find folder /gameserver and /messagebroker

Do the above for one machine. The two others wont a need messagebroker, but do need a gameserver.

### Starting a messagebroker

1. `cd messagebroker`
2. `python3 main.py 3000` will start the messagebroker in the port 3000.

### Starting a load balancer

1. `cd loadbalancer`
2. Store the ip-addresses of the machines gameservers will be deployed to `servers.txt` (one ip per line)
2. `python3 main.py 7800` will start the loadbalancer in the port 7800.

### Starting a gameserver

0. Store the ip-address of the machine messagebroker was deployed to `messagebroker.txt`
1. `cd gameserver`
2. Create a virtual environment `python3 -m venv .venv` (if not done already)
3. `source .venv/bin/activate && pip install -r requirements.txt`
4. Start the server with `source start.sh`

