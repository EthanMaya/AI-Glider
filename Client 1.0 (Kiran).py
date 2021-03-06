from socket import AF_INET, socket, SOCK_STREAM, IPPROTO_TCP, TCP_NODELAY
from threading import Thread
from time import sleep

"""Guide to telemetry and control (fold code to hide):
    Controller:
    0 - Bank (+ is right)
    1 - Pitch (+ is down)
    2 - Rudder (+ is right)
    3 - Engine Power (+ is more)

    Telemetry basics:
        Example (newlines added for clarity):
        ===
            Agent 0 Telemetry time 432.067169
            pos -104.679298 146.436508 96.640022
            faceDir -0.956105 -0.292488 0.017743
            upDir 0.022083 -0.011543 0.999689
            alt 50.356339
            vel -4.029115 -1.590821 1.015002
            wind 10.357739 3.192868 0.451366
        ===
        Composition:
        ===
            Agent {agent} Telemetry time {time}
            pos {px} {py} {pz}
            faceDir {fx} {fy} {fz}
            upDir {ux} {uy} {uz}
            alt {a}
            vel {vx} {vy} {vz}
            wind {wx} {wy} {wz}
        ===
        Variable explanation:
            agent - the number of the plane (in our case 0)
            time - the time since the program started (NOT the python script)
            px, py, pz - the x, y, and z coordinates of the plane
                            On Cliff scenery, +x is backwards I think
            fx, fy, fz - the direction the plane is facing.
                            fx - sine of the heading
                            fy - cosine of the heading
                            fz - sine of the pitch
                            this direction is outputted in quite a frustrating way:
                                    fx  fy
                            North -  0   1
                            East  -  1   0
                            South -  0  -1
                            West  - -1   0
                            On the Cliff scenery, the aircraft takes off towards the west, with the wind going east
            ux, uy, uz - not sure what this does, probably the direction to the zenith of the aircraft
            a - altitude of the aircraft in m
            vx, vy, vz - velocity of the aircraft (groundspeed I think) as a matrix
                            vz - + is up, - is down
                                    vx  vy
                            North - 0   +
                            East  - +   0
                            South - 0   -
                            West  - -   0
            wx, wy, wz - wind speed relative to the aircraft
"""

class Receiver: # so thread can be conveniently terminated
    def __init__(self, sock, BUFSIZ):
        self.sock = sock
        self.BUFSIZ = BUFSIZ
        self.keepReceiving = True
        self.telemetry = {}
    def close(self):
        self.keepReceiving = False
    def getTelemetry(self):
        return self.telemetry
    def receive(self):
        while self.keepReceiving:
            try:
                msg = self.sock.recv(self.BUFSIZ).decode("utf8")
                if not msg:
                    print("Receive thread: Received empty data - closing connection\n")
                    self.close()
                    break
                self.telemetry = {
                    "pos":      msg.split("pos")[1].split(" ")[1:4],
                    "faceDir":  msg.split("faceDir")[1].split(" ")[1:4],
                    "upDir":    msg.split("upDir")[1].split(" ")[1:4],
                    "alt":      msg.split("alt")[1].split(" ")[1],
                    "vel":      msg.split("vel")[1].split(" ")[1:4],
                    "wind":     msg.split("wind")[1].split(" ")[1:4]
                }
            except Exception as e:
                if self.keepReceiving:
                    print("Receive thread: receive error\n", e)
                    break

def send(msg):
    msg += "\n" # Needed for PicaSim
    sock.send(bytes(msg, "utf8"))

def close(receiver):
    send("requesttelemetry 0")
    send("releasecontrol")
    send("pause")
    send("reset")
    receiver.close()
    sock.close()
    print("Socket Closed")

def pause():
    send("pause")
def resume():
    send("unpause")
def control():
    send("agent 0")
    send("takecontrol")

HOST = "127.0.0.1"
PORT = 7777
BUFSIZ = 1024
ADDR = (HOST, PORT)
sock = socket(AF_INET, SOCK_STREAM)
sock.setsockopt(IPPROTO_TCP, TCP_NODELAY, 1)
while True:
    try:
        sock.connect(ADDR)
        break
    except:
        print("Main thead: Connection error. Maybe PicaSim is not running?")
        print("Make sure you have enabled port controlling in PicaSim settings.")
        input("Press enter to retry connection.\n")

receiver = Receiver(sock, BUFSIZ)
receive_thread = Thread(target=receiver.receive)
receive_thread.start()

print("Running")
send("reset")
resume()

# Custom code here
send("requesttelemetry 0.1")
#send("releasecontrol")
control()
tel = {}





"""i = 0
requiredPitch = 0.3
requiredHVelocity = 8
while True:
    tel = receiver.getTelemetry()
    if tel.get("faceDir") == None:
        print("Main thread: No data received.")
        sleep(0.5)
        continue
    print(float(tel.get("upDir")[2]))
    hvelocity = (float(tel.get("vel")[0]) ** 2 + float(tel.get("vel")[1]) ** 2) ** 0.5
    vvelocity = float(tel.get("vel")[2])
    if vvelocity < -1 and pitch > 0.1:
        print("STALL")
        requiredHVelocity += 0.1
    elif vvelocity > 1:
        requiredHVelocity -= 1
    relativeHVelocity = hvelocity - requiredHVelocity
    if abs(relativeHVelocity) > 0:
        if relativeHVelocity > 0:
            #print("too fast, decreasing speed %i" % i)
            send("control 3 -%f" % 0.2)
            requiredPitch += 0.01
            i += 1
        else:
            #print("too slow, increasing speed %i" % i)
            send("control 3 %f" % 0.2)
            requiredPitch -= 0.01
            i += 1
    pitch = float(tel.get("faceDir")[2])
    relativePitch = pitch - requiredPitch
    if abs(relativePitch) > 0.01:
        if relativePitch > 0:
            send("control 1 %f" % (abs(relativePitch) - 0.01))
            #print("Main thead: adjusting up %i" % i)
            i += 1
        else:
            send("control 1 -%f" % (abs(relativePitch) - 0.01))
            #print("Main thread: adjusting down %i" % i)
            i += 1
    
    sleep(0.1)"""

# Custom code ends here

close(receiver)
print("Closed")
