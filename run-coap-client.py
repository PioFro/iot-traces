import os
import time
import random
import coapconfig as config
import requests

def getIps():
    tmp = []
    r = requests.get("http://{}:5000/operation/show/".format(config.IPMANAGERIP))
    spl = r.text.split(",")
    for ip in spl:
        if ip != config.MYIP+"S":
            tmp.append(ip)
    return tmp
file=open("test.txt","w")

numberWithoutRQ = 1
serverips=getIps()
types=["block-get","block-put","separate","time"]

density = 1000
sleeptime = 1

print("configuration of the CoAP client simulator complete.\n COAP SERVERS:{}, \n COAP RQ TYPES: {} \n DENSITY: {} \n SLEEP BETWEEN TRIES: {} \n\n".format(serverips,types,str(density),str(sleeptime)))
while True:
    print("Send msg? ->")
    if random.randint(0,density) < numberWithoutRQ:
        print("yes\n")
        type = random.randint(0, len(types)-1)
        ip = random.randint(0,len(serverips)-1)
        serverips
        print("python3 coap-client.py {} {}".format(serverips[ip],types[type]))
        os.system("python3 coap-client.py {} {}".format(serverips[ip],types[type]))
        file.write(str(numberWithoutRQ)+"\n")
        numberWithoutRQ = 1
    else:
        print("NO! \nChance: {}/{}".format(numberWithoutRQ,density))
        numberWithoutRQ+=1
    try:
        time.sleep(sleeptime)
    except:
        file.close()
        exit(0)