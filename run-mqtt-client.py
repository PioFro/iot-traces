from mqttClient import Client
import psutil

c = Client()
c.setInfoFunction(psutil.cpu_percent)
c.start()
c.publishAll()
c.subscribeAll()

