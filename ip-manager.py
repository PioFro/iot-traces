from flask import Flask

app = Flask(__name__)

class IpManager:
    ReservedIps = []
    InitDone = False
    @staticmethod
    def init(initialReservedIps):
        IpManager.ReservedIps = initialReservedIps
        IpManager.InitDone = True

    @staticmethod
    def checkIp(ip):
        for addr in IpManager.ReservedIps:
            if ip == addr:
                return False
        return True
    @staticmethod
    def registerIp(ip):
        if IpManager.checkIp(ip):
            IpManager.ReservedIps.append(ip)

@app.route("/init/")
def init():
    if IpManager.InitDone == False:
        print("INITIALIZING...")
        file = open("venv/db/ip-list")
        tmp = []
        for line in file:
            tmp.append(line.replace("\n",""))
        IpManager.init(tmp)
        print("Initialized with a list of ips {}".format(tmp))
        file.close()
        return "OK"
    else:
        return "Already initialized with ips {}".format(IpManager.ReservedIps)

@app.route("/newip/<ipmask>/")
def getNewIpForSubnet(ipmask):
    print("Fetching new ip for mask of ip {}".format(ipmask))
    mask = ipmask.split(".")
    countX = ipmask.count("x")
    if countX == 0:
        try:
            for tet in mask:
                t = int(tet)
        except:
            return "WRONG FORMAT OF IP {}".format(ipmask)

        if IpManager.checkIp(ipmask):
            IpManager.registerIp(ipmask)
            return "IP ADDR:{}".format(ipmask)
        else:
            return "IP ADDR:0.0.0.0"
    for i in range(1,255):
        if countX > 1:
            for j in range(1,255):
                if IpManager.checkIp("{}.{}.{}.{}".format(mask[0],mask[1],j,i)):
                    IpManager.registerIp("{}.{}.{}.{}".format(mask[0],mask[1],j,i))
                    return "IP ADDR:{}.{}.{}.{}".format(mask[0],mask[1],j,i)
        else:
            if IpManager.checkIp("{}.{}.{}.{}".format(mask[0], mask[1], mask[2], i)):
                IpManager.registerIp("{}.{}.{}.{}".format(mask[0], mask[1], mask[2], i))
                return "IP ADDR:{}.{}.{}.{}".format(mask[0], mask[1], mask[2], i)
    return "IP ADDR:0.0.0.0"
@app.route("/operation/<code>/")
def end(code):
    print("Registered special signal "+code)
    if code == "delete":
        IpManager.ReservedIps = []
        file = open("venv/db/ip-list", "w")
        file.truncate()
        file.close()
    if code == "backup":
        file = open("venv/db/backup-ip-list.safe", "w")
        for ip in IpManager.ReservedIps:
            file.write(ip+"\n")
        file.close()
    if code == "show":
        r = ""
        return str(IpManager.ReservedIps).replace("[","").replace("]","").replace("'","").replace(" ","")

    return "Operation with code {} successful".format(code)


if __name__ == '__main__':
    app.run(host="0.0.0.0")
