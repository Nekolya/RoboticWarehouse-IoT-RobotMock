import paho.mqtt.client as mqtt
import asyncio

class Robot():

    async def publish(self, client):
        while True:
            await asyncio.sleep(10)
            client.publish("robots/data", "Hello world!")
            print("published")

    async def connect(self, client):
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

        
        client.connect_async("localhost",1883,60)
        client.on_connect = on_connect
        client.on_message = on_message
        await client.loop_start()

    async def main(self):
        client = mqtt.Client()
        input_coroutines = [self.connect(client), self.publish(client)]
        res = await asyncio.gather(*input_coroutines, return_exceptions=True)
        print('Can i do somthing?')