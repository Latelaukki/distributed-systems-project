import os
from fastapi import FastAPI, Request, Response
from services.database import init_db, get_messages, store_message, consume_powerup_db, populate_powerups_db
from services.messagebroker import Messagebroker
import uuid
import json

SERVER_ID = uuid.uuid4()
DB_FOLDER = "./DB"
DB_PATH = f"{DB_FOLDER}/{SERVER_ID}.db"
EXCHANGE = "events"
POWER_UP_EXCHANGE = "power_up"
TOPICS = [EXCHANGE, POWER_UP_EXCHANGE]
MYIP = "localhost"
PORT = "7777"
MESSAGEBROKER_IP = "http://localhost:3000/listen"

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
   data = { "ip": MYIP, "port": PORT, "path": "messages", "topic": topic }
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
      consume_powerup_db()
      return {"ok"}
   
   if message_parsed["topic"] == EXCHANGE:
      store_message({ "msg": f"{message_parsed['message']}", "db_path": DB_PATH })
      return {"ok"}
   
   
   return {f"Not subscribed to {message_parsed['topic']}"}


@app.get("/get-maze/{maze_id}/{player_id}")
def get_maze(maze_id: str, player_id: str):
   message = f"Player {player_id} requested maze {maze_id} from {SERVER_ID}"
   # Make another thread for publishing the message to rabbitmq
   #start_new_publish_thread(EXCHANGE,message)
   msgbroker.publish(EXCHANGE,message)
   return {f"Returned maze ({maze_id}) |---|--|----| from {SERVER_ID}"}

@app.post("/consume-powerup/")
async def consume_powerup(request: Request):
   message = await request.body()
   msgbroker.publish(POWER_UP_EXCHANGE,message)
   #start_new_publish_thread(POWER_UP_EXCHANGE,message)
   return {f"consumed powerup: {message}"}

@app.get('/get-server')
def main(request: Request):
    host_url = request.headers.get('host')
    return {f"This is server {host_url}"}