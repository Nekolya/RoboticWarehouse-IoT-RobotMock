import paho.mqtt.client as mqtt
import asyncio
import os
import json


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
                    "target": file_data["target"],
                    "location": file_data["location"],
                    "charge": file_data["charge"],
                    "products": file_data["products"]
                }
                
                print('Already init')

        if not os.path.exists('robots_data/'):
            os.mkdir('robots_data/')

        self.data = {
            "id": id,
            "model": model,
            "status": status,
            "target": None,
            "location": location,
            "charge": charge,
            "products": []}

        with open('robots_data/data' + str(id) + '.json', 'w') as f:
            json.dump(self.data, f)


    async def publish(self):
        while True:
            await asyncio.sleep(5)
            self.client.publish("robots/data", json.dumps(self.data))
            print("published")

    async def connect(self):
        def on_message(client, userdata, message):
        #   if message.payload.decode() == "Hello world!":
            print("message received", str(message.payload.decode("utf-8")))
            print("message topic=",message.topic)
            # print("message qos=",message.qos)
            # print("message retain flag=",message.retain)
            # print('userdata', userdata)
            # print('client', client)

        def on_connect(client, userdata, flags, rc):
            print("Connected with result code "+ str(rc))
            client.subscribe("robots/tasks")

        
        
        self.client.connect_async("localhost",1883,60)
        self.client.on_connect = on_connect
        self.client.on_message = on_message
        await self.client.loop_start()

    async def main(self):
        input_coroutines = [self.connect(), self.publish()]
        res = await asyncio.gather(*input_coroutines, return_exceptions=True)
        print('Can i do somthing?')