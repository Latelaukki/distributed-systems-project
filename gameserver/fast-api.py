import os
from fastapi import FastAPI, Request, Response
from services.database import init_db, get_messages, store_message, consume_powerup_db, populate_powerups_db
from services.messagebroker import Messagebroker
import uuid
import json
import subprocess
import sys

SERVER_ID = uuid.uuid4()
DB_FOLDER = "./DB"
DB_PATH = f"{DB_FOLDER}/{SERVER_ID}.db"
EXCHANGE = "events"
ELECTION = "election"
POWER_UP_EXCHANGE = "power_up"
CONSENSUS = "consensus"
TOPICS = [EXCHANGE, CONSENSUS, POWER_UP_EXCHANGE, str(SERVER_ID)]
PORT = "7777"
MESSAGEBROKER_IP = "http://localhost:3000"
LOCAL_LOG = {"Speed" : "available"}
RESPONSE_TOPIC = str(SERVER_ID)
RESPONSES = []

PORT = sys.argv[-1]
print(f"Gameserver starting in port {PORT}")

# kokeillaan löytyykö messagebrokerin ip:tä levyltä

msgbroker_ip_file = "messagebroker.txt"
if os.path.exists(msgbroker_ip_file):
   with open(msgbroker_ip_file, "r") as f:
      ip = f.read().replace("\n", "")
      MESSAGEBROKER_IP = f"http://{ip}:3000"
      print(f"Read msgbroker ip from disk ({MESSAGEBROKER_IP})")

# ip-osoite
cmd_hostname = subprocess.run(['hostname', '-I'], stdout=subprocess.PIPE)
myip = str(cmd_hostname.stdout, encoding="utf-8").replace("\n", "").replace(" ", "")
#myip = 'localhost'

# Luodaan kansio tietokantaa varten. Subscribe kirjoittaa saapuneet viestit ko. kansiossa olevaan kantaan
if not os.path.exists(DB_FOLDER): 
    os.makedirs(DB_FOLDER) 

# Alustetaan tietokanta
init_db(DB_PATH)
populate_powerups_db(DB_PATH)


# Messagebroker
msgbroker = Messagebroker(MESSAGEBROKER_IP)

# Viestitään messagebrokerirille, että halutaan kuunnella topicceja 
for topic in TOPICS:
   # Kerrotaan messagebrokerille, että tämä ip-osoitteesta ja portista haluaa kuunnella viestejä tietyn topicin alta
   # Kun messagebroker saa viestin ko. topicciin, se lähettää sen tälle osoitteeseen ip:port/path
   data = { "ip": myip, "port": PORT, "path": "messages", "topic": topic }
   msgbroker.listen(data)



app = FastAPI()


@app.get("/")
def read_root():
   return {"Hello": "World"}


@app.get("/messages")
def read_root():
   messages = get_messages(DB_PATH)

   list = ''.join([
      f"<li>{msg}</li>" for msg in messages
   ])

   html = f"""
      <html>
      <body>
      <h3>Messages from server {SERVER_ID}</h3>
      <ul>
         {list}      
      </ul>
      </body>
      </html>    

   """
   return Response(content=html, media_type="text/html")


@app.post("/messages")
async def handle_message(request: Request):
   # This will collect all messages from the messagebroker
   message = await request.body()
   message_parsed = json.loads(message)

   topic = message_parsed["topic"]
   msg_content = message_parsed['message']

   if topic == str(SERVER_ID):
      print(f"Received answer '{msg_content}' to consensus request")
      if msg_content == "available":
         RESPONSES.append(msg_content)

   if topic == POWER_UP_EXCHANGE:
      consume_powerup_db({ "msg": f"{msg_content}", "db_path": DB_PATH })
      return {"ok"}
   
   if topic == EXCHANGE:
      store_message({ "msg": f"{msg_content}", "db_path": DB_PATH })
      return {"ok"}
   
   if topic == CONSENSUS:
      uuid = msg_content
      if uuid == str(SERVER_ID):
         # Request is from self. No need to do anything.
         return {"ok"}
      
      if LOCAL_LOG["Speed"] == "available":
         message = "available"
      else:
         message = "unavailable"

      # Update status of self
      LOCAL_LOG["Speed"] == "unavailable"

      print(f"Responding '{message}' to consensus request from {uuid}")
      msgbroker.publish(uuid, message)
      return {"ok"}
   

   return {f"Not subscribed to {message_parsed['topic']}"}


@app.post("/consume-powerup/")
async def consume_powerup(request: Request):
   message = await request.body()
   message = message.decode("utf-8")
   message_parsed = json.loads(message)
   msgbroker.publish(CONSENSUS,str(SERVER_ID))
   LOCAL_LOG["Speed"] = "unavailable"
   return {f"consumed powerup: {message_parsed}"}

@app.get('/power-up-available/')
def power_available(request: Request):
   status = LOCAL_LOG["Speed"]

   if len(RESPONSES) > 0 and LOCAL_LOG["Speed"] == "unavailable":
      return "available"
   if LOCAL_LOG["Speed"] == "unavailable":
      return "unavailable"

   return "pending"

@app.get('/get-server')
def main(request: Request):
   host_url = request.headers.get('host')
   return {f"This is server {host_url}"}
