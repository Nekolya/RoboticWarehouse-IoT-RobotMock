import paho.mqtt.client as mqtt
import asyncio
import os
import json
from random import randint


class Robot():
    def __init__(self, id, model, status, location, charge):
        self.client = mqtt.Client()
        if os.path.exists('robots_data/data' + str(id) + '.json'):

            with open('robots_data/data' + str(id) + '.json', 'r') as f:
                file_data = json.load(f)
                self.data = {
                    "id": file_data["id"],
                    "model": file_data["model"],
                    "status": file_data["status"],
                    "area": file_data["area"],
                    "charge": file_data["charge"],
                    "product": file_data["product"],
                    "way": file_data["way"],
                    "order": file_data["order"],
                    "took": file_data["took"]
                }

                print('Already init')

        if not os.path.exists('robots_data/'):
            os.mkdir('robots_data/')

        self.data = {
            "id": id,
            "product": None,
            "model": model,
            "charge": charge,
            "way": None,
            "status": status,
            "area": location,
            "order": None,
            "took": False
        }
        with open('robots_data/data' + str(id) + '.json', 'w') as f:
            json.dump(self.data, f)

    async def publish(self):
        while True:
            if (not self.data["way"]):
                self.data["status"] = 1
            await asyncio.sleep(30)
            self.client.publish("robots/data", json.dumps(self.data))
            print("published")

    async def moving(self):
        while True:
            await asyncio.sleep(2)
            if self.data["way"]:
                area = self.data["way"].pop(0)
                if not len(self.data["way"]):
                    self.data["way"] = None
                    self.data["status"] = 1
                if area == 5 and self.data["status"] == 5:
                    self.data["status"] = 1
                    self.client.publish(
                        "robots/finish", json.dumps(
                            {'id': self.data['id'], 
                             'order': self.data['order']}))
                    self.data['order'] = None
                self.data["area"] = area
                await asyncio.sleep(randint(2, 3))
                # print("published move")
                self.client.publish("robots/data", json.dumps(self.data))

    async def connect(self):
        def on_message(client, userdata, message):
            #   if message.payload.decode() == "Hello world!":
            print("message received", str(message.payload.decode("utf-8")))
            print("message topic=", message.topic)
            data = json.loads(message.payload.decode("utf-8"))
            print(data["id"] == self.data["id"], "data[id] == self.data[id]")
            if data["id"] == self.data["id"]:
                self.data["way"] = data["way"]
                self.data["status"] = 5
                self.data["order"] = data["order"]
                print(self.data["way"])
                
            # print("message qos=",message.qos)
            # print("message retain flag=",message.retain)
            # print('userdata', userdata)
            # print('client', client)

        def on_connect(client, userdata, flags, rc):
            print("Connected with result code " + str(rc))
            client.subscribe("robots/tasks")

        self.client.connect_async("localhost", 1883, 60)
        self.client.on_connect = on_connect
        self.client.on_message = on_message
        await self.client.loop_start()

    async def main(self):
        input_coroutines = [self.connect(), self.publish(), self.moving()]
        res = await asyncio.gather(*input_coroutines, return_exceptions=True)
        print('Can i do somthing?')
