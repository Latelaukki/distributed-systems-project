# Instructions on how to deploy HY-machines

Setup connection and copy files using this guide:

    https://helpdesk.it.helsinki.fi/en/instructions/logging-and-connections/using-cubbli-workstation-home-computer#using-cubbli-on-a-linux-home-computer

Specically follow guidelines from `If you also need to copy files between your home ...` onwards.

After configuring something like this:

    ssh -f -N -q pangtunnel 
    scp -r gameserver/*.* duuni1:
    scp -r gameserver/services duuni1:
    scp -r messagebroker/ duuni1:
    scp -r loadbalancer/ duuni1:

You should find folder /gameserver and /messagebroker

Do the above for one machine. The two others wont a need messagebroker.

# Start a messagebroker

0. Find out the ip of the server using `ip a`
1. `cd messagebroker`
2. `python3 main.py 3000` will start the messagebroker in the port 3000.

# Starting a gameserver

0. store the ip-address of messagebroker to messagebroker.txt
1. `cd gameserver`
2. `python3 -m venv .venv` (if not done already)
3. `source .venv/bin/activate && pip install -r requirements.txt`
4. Start the server with `source start.sh`

        

# Testing

When you start the gameserver it will listen to power ups and events (by telling the messagebroker so).

After you have a messagebroker and gameservers up, you can send a request to one of the gameservers and see what happens:

    curl 123.123.123.123:7777/get-maze/1/1234
