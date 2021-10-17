import paho.mqtt.client as mqtt
import time
import asyncio
from random import randint


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
    client.subscribe("topic/test")

async def publish(client):
    while True:
        await asyncio.sleep(5)
        client.publish("topic/test", "Hello world!")
        print("published")

async def connect(client):
    client.connect_async("localhost",1883,60)
    client.on_connect = on_connect
    client.on_message = on_message
    await client.loop_start()

async def main():
    client = mqtt.Client()
    input_coroutines = [connect(client), publish(client)]
    res = await asyncio.gather(*input_coroutines, return_exceptions=True)
    print('Can i do somthing?')


if __name__ ==  '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())