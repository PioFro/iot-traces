import json
import random
import paho.mqtt.client as mqtt
import psutil
import threading
import time, traceback

def every(delay, task, **kwargs):
  next_time = time.time() + delay
  while True:
    time.sleep(max(0, next_time - time.time()))
    try:
      task(**kwargs)
    except Exception:
      traceback.print_exc()
    next_time += (time.time() - next_time) // delay * delay + delay

class Client:
    def __init__(self):
        configFile = open("mqtt-config.json", "r")
        jConfig = json.loads(configFile.read())

        self._id = jConfig["id"]+":"+str(hex(int(str(random.random()).replace(".",""))))
        self._brokerIp = jConfig["broker ip"]
        self._qos = jConfig["qos"]
        self._subtopics = []
        self._pubtopics = []


        for topic in jConfig["sub topics"]:
            self._subtopics.append(topic)

        for topic in jConfig["pub topics"]:
            spt = str(topic).split("-")
            self._pubtopics.append((spt[0], spt[1]))

        self._rawMQTTClient=mqtt.Client(self._id)
        self.connect()
        self._rawMQTTClient.on_message = on_message
        self._sentInfoFunction = getInfo

    def connect(self):
        self._rawMQTTClient.connect(self._brokerIp)
    def publishAll(self):
        for pub in self._pubtopics:
            threading.Thread(target=lambda : every(int(pub[1]),self.publishSingle,topic=pub[0],value=self._sentInfoFunction,qos=self._qos)).start()

    def publishSingle(self, **kwargs):
        topic = kwargs.get("topic")
        value = kwargs.get("value")
        qos = kwargs.get("qos")
        self._rawMQTTClient.publish(topic,value(),qos)

    def subscribeAll(self):
        for sub in self._subtopics:
            self._rawMQTTClient.subscribe(sub,self._qos)

    def start(self):
        self._rawMQTTClient.loop_start()
    def stop(self):
        self._rawMQTTClient.loop_stop()

    def setInfoFunction(self, f):
        try:
            f()
        except:
            print("Provided argument isn't a function.")
            return
        self._sentInfoFunction = f


def on_message(client, userdata, message):
    print(userdata)
    try:
        json.loads(message.payload.decode("utf-8"))
        print("JSON correct")
    except Exception:
        print("Not able to prase to JSON. "+str(Exception))
    print("message received " ,str(message.payload.decode("utf-8")))
    print("message topic=",message.topic)
    print("message qos=",message.qos)
    print("message retain flag=",message.retain)

def getInfo():
    info = dict()
    info["cpu_usage"] = psutil.cpu_percent()
    info["memory_usage"] = str(psutil.virtual_memory())
    info["swap_size"] = str(psutil.swap_memory())
    info["disk usage"]=str(psutil.disk_usage("/home/"))
    info["ifaces"]=str(psutil.net_if_addrs().keys())
    return str(json.dumps(info))