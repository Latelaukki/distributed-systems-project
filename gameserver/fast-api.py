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
TOPICS = [EXCHANGE, CONSENSUS, POWER_UP_EXCHANGE]
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
myip = 'localhost'

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

   if message_parsed["topic"] == POWER_UP_EXCHANGE:
      consume_powerup_db({ "msg": f"{message_parsed['message']}", "db_path": DB_PATH })
      return {"ok"}
   
   if message_parsed["topic"] == EXCHANGE:
      store_message({ "msg": f"{message_parsed['message']}", "db_path": DB_PATH })
      return {"ok"}
   
   if message_parsed["topic"] == CONSENSUS:
      if LOCAL_LOG["Speed"] == "available":
         message = {"message" : "available"}
      else:
         message = {"message" : "unavailable"}
      msgbroker.publish(RESPONSE_TOPIC, message)
      return {"ok"}
   
   if message_parsed["topic"] == RESPONSE_TOPIC:
      RESPONSES.append(message_parsed["message"])
      if len(RESPONSES) == 3:
         if "unavailable" not in RESPONSES:
            msgbroker.publish(POWER_UP_EXCHANGE,message)
            return {"ok"}

   return {f"Not subscribed to {message_parsed['topic']}"}


@app.post("/consume-powerup/")
async def consume_powerup(request: Request):
   message = await request.body()
   message = message.decode("utf-8")
   message_parsed = json.loads(message)
   msgbroker.publish(POWER_UP_EXCHANGE,message_parsed)
   return {f"consumed powerup: {message_parsed}"}

@app.get('/get-server')
def main(request: Request):
   host_url = request.headers.get('host')
   return {f"This is server {host_url}"}

@app.post("/consensus")
async def consensus(request: Request):
   message = await request.body()
   message = message.decode("utf-8")
   message_parsed = json.loads(message)
   if message_parsed["data"] == "Speed":
      LOCAL_LOG["Speed"] == "unavailable"

   data = {"ip": myip, "port": PORT, "path": "messages", "topic": RESPONSE_TOPIC}
   msgbroker.listen(data)

   msgbroker.publish(CONSENSUS, message)
   return {f"Waiting for responses: {message}"}
