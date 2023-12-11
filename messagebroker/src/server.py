import json
import requests
from http.server import HTTPServer, BaseHTTPRequestHandler
from threading import Thread

# Tämä kerää tietyn topicin kuuntelijat. Esim:
#   {
#       "power_up": {
#               "127.0.0.0_80_messages": (127.0.0.0,80)
#           }
#   } 
#
#
topics = {}

def post_message(target, message):
    requests.post(target, json=message)

def new_post_message_thread(target, message):
   post_thread = Thread(target=post_message, args=[target,message])
   post_thread.start()

def respond_ok(srvr):
    srvr.send_response(200)
    srvr.end_headers()

def handle_root(srvr):
    respond_ok(srvr)


def handle_listen(srvr):

    content_length = int(srvr.headers['Content-Length'])
    data = srvr.rfile.read(content_length)
    print("Received data: ", data.decode('utf-8'))
    data_encoded = json.loads(data.decode('utf-8'))
    
    topic   = data_encoded['topic']
    ip_port_path = (
        data_encoded['ip'],
        str(data_encoded['port']),
        data_encoded["path"]
    )

    key = '_'.join(ip_port_path)

    if topic not in topics:
        topics[topic]  = { key: ip_port_path }
    else:
        topics[topic][key] = ip_port_path

    print(f"{ip_port_path} is listening to {topic}")
    respond_ok(srvr)




def handle_message(srvr):
    content_length = int(srvr.headers['Content-Length'])
    data = srvr.rfile.read(content_length)
    
    # _oletetaan, että tulee validia JSON:ia, joka sisältää attribuutit: topic, message
    data_encoded = json.loads(data.decode('utf-8'))
    topic   = data_encoded['topic']
    message = data_encoded['message']

    if topic not in topics:
        print("Nobody listens to this topic")
        respond_ok(srvr)
        return
    
    
    for key in topics[topic].keys():
        
        ip, port, path = topics[topic][key]

        target = f"http://{ip}:{port}/{path}"
        
        print(f"Posting {message} under topic {topic} to {target}")
        try:
            new_post_message_thread(target, data_encoded)
        except Exception as error:
            print(f"Could not connect to {target}: ", error)

    respond_ok(srvr)
    



handlers  = {
    "GET": {
        "/": handle_root
    },
    "POST": {
        "/": handle_root,
        "/listen": handle_listen,
        "/message": handle_message

    }
}



class Messagebroker(BaseHTTPRequestHandler):


    def do_GET(self):
        print(f"GET {self.path}")
        try:
            handler = handlers["GET"][self.path]
        except KeyError:
            print("Defaulting")
            handler = handlers["GET"]["/"]

        handler(self)
        
    def do_POST(self):
        print(f"POST {self.path}")
        try:
            handler = handlers["POST"][self.path]
        except KeyError:
            print("Defaulting")
            handler = handlers["POST"]["/"]

        handler(self)
        


def run(port, server_class=HTTPServer, handler_class=Messagebroker):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)    
    httpd.serve_forever()