import requests


class Messagebroker:

    def __init__(self, ip):
        self.ip = ip
    

    def publish(self, topic, message):
        requests.post(self.ip,json={ "message": message, "topic": topic })


    def listen(self, data):
        requests.post(self.ip,json=data)
