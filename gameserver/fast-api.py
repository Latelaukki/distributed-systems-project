import os
from fastapi import FastAPI, Request, Response
from services.publish import  publish, consume_powerup
from services.subscribe import subscribe
from services.database import init_db, get_messages, store_message, consume_powerup_db, populate_powerups
import uuid
from threading import Thread

SERVER_ID = uuid.uuid4()


DB_FOLDER = "./DB"
DB_PATH = f"{DB_FOLDER}/{SERVER_ID}.db"
EXCHANGE = "events"
POWER_UP_EXCHANGE = "power_up"

# Luodaan kansio tietokantaa varten. Subscribe kirjoittaa saapuneet viestit ko. kansiossa olevaan kantaan
if not os.path.exists(DB_FOLDER): 
    os.makedirs(DB_FOLDER) 

# Alustetaan tietokanta
init_db(DB_PATH)
populate_powerups(DB_PATH)

# Käynnistetään oma threadi rabbitMQ:n pollaamiseen.
# Ikuinen looppi, joten pitää olla omassa threadissa
# Koska pyörii omassa threadissa, niin logit ei näy

def callback(ch, method, properties, body):
   store_message({ "msg": f"{body}", "db_path": DB_PATH })

def consume_powerup_callback(ch, method, properties, body):
   consume_powerup_db({ "msg": f"{body}", "db_path": DB_PATH })

subscribeThread = Thread(target=subscribe, args=[EXCHANGE, callback])
subscribeThread2 = Thread(target=subscribe, args=[POWER_UP_EXCHANGE, consume_powerup_callback])
subscribeThread.start()
subscribeThread2.start()



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


@app.get("/get-maze/{maze_id}/{player_id}")
def get_maze(maze_id: str, player_id: str):

   message = f"Player {player_id} requested maze {maze_id} from {SERVER_ID}"
   
   # Make another thread for publishing the message to rabbitmq
   publishThread = Thread(target=publish, args=[EXCHANGE,message])
   publishThread.start()

   return {f"Returned maze ({maze_id}) |---|--|----| from {SERVER_ID}"}

@app.post("/consume-powerup/")
async def consume_powerup(request: Request):
   data = await request.body()
   print('data was ', data)

   #message = f""
   # Make another thread for publishing the message to rabbitmq
   publishThread = Thread(target=publish, args=[POWER_UP_EXCHANGE,data])
   publishThread.start()

   return {f"SENT POWERUP CONSUMED"}

@app.get('/get-server')
def main(request: Request):
    host_url = request.headers.get('host')
    return {f"This is server {host_url}"}