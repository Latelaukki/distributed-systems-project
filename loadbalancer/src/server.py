import os
from http.server import HTTPServer, BaseHTTPRequestHandler

SERVERFILE = "servers.txt"

if not os.path.exists(SERVERFILE):
    print(f"Need to specify {SERVERFILE}")
    exit(0)

with open(SERVERFILE, "r") as f:
    servers = [ l.replace("\n", "") for l in f.readlines() if len(l) > 0  ]

def get_server():
    server = servers.pop(0)
    servers.append(server)
    return server

def respond_ok(srvr):
    srvr.send_response(200)
    srvr.end_headers()

class LoadBalancer(BaseHTTPRequestHandler):
    def do_GET(self):
        respond_ok(self)
        self.wfile.write(bytes(get_server(), encoding='UTF-8'))
        


def run(port, server_class=HTTPServer, handler_class=LoadBalancer):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)    
    httpd.serve_forever()


if __name__ == "__main__":
    for i in range(5):
        print(get_server())