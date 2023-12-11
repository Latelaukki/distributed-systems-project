import requests


class Messagebroker:

    def __init__(self, ip):
        self.ip = ip
    

    def publish(self, topic, message):
        try:
            requests.post(self.ip + "/message",json={ "message": message, "topic": topic })
        except Exception as error:
            print("Failed to publish to msgbroker:", error)



    def listen(self, data):
        requests.post(self.ip + "/listen",json=data)
