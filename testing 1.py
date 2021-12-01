from threading import Thread

class Receiver:
    def __init__(self):
        self.keepReceiving = True
        self.telemetry = {}
    def close(self):
        self.keepReceiving = False
    def getTelemetry(self):
        return self.telemetry
    def receive(self):
        while self.keepReceiving:
            try:
                msg = "pos 1 1 1"
                self.telemetry = {
                    "pos":      msg.split("pos")[1].split(" ")[1:4]
                }
                print(self.telemetry)
            except Exception as e:
                if self.keepReceiving:
                    print("receive error\n", e)
                    break
receiver = Receiver()
receive_thread = Thread(target=receiver.receive)
receive_thread.start()

while True:
    tel = receiver.getTelemetry()
    #print(tel)