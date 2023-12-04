from services.publish import  publish
from threading import Thread

def start_new_publish_thread(exhange, message):
   publishThread = Thread(target=publish, args=[exhange,message])
   publishThread.start()

