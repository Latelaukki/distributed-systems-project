import os
from fastapi import FastAPI, Request, Response
from services.publish import  publish
from services.subscribe import subscribe
from services.database import init_db, get_messages
import uuid
from threading import Thread

SERVER_ID = uuid.uuid4()


DB_FOLDER = "./DB"
DB_PATH = f"{DB_FOLDER}/{SERVER_ID}.db"

# Luodaan kansio tietokantaa varten. Subscribe kirjoittaa saapuneet viestit ko. kansiossa olevaan kantaan
if not os.path.exists(DB_FOLDER): 
    os.makedirs(DB_FOLDER) 

# Alustetaan tietokanta
init_db(DB_PATH)

# Käynnistetään oma threadi rabbitMQ:n pollaamiseen.
# Ikuinen looppi, joten pitää olla omassa threadissa
# Koska pyörii omassa threadissa, niin logit ei näy
subscribeThread = Thread(target=subscribe, args=[SERVER_ID, DB_PATH])
subscribeThread.start()



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
   publishThread = Thread(target=publish, args=[message])
   publishThread.start()

   return {f"Returned maze ({maze_id}) |---|--|----| from {SERVER_ID}"}

@app.get('/get-server')
def main(request: Request):
    host_url = request.headers.get('host')
    return {f"This is server {host_url}"}