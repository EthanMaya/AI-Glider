from socket import AF_INET, socket, SOCK_STREAM, IPPROTO_TCP, TCP_NODELAY
from threading import Thread
from time import sleep

# NOTE: rudder, pitch, bank reset if not being sent data,
#       so need to send data constantly, so remove if statements

# TODO: split basic controllers (bank, pitch, rudder, engine)
#       from advanced detection (altitude, stall, speed)


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
            ux, uy, uz - see below
                            uz - bank - 1 is no bank, 0.5 is 45 degree bank
                            uy - bank - 0 is no bank, 1 is bank to the right, -1 is bank to the left (I think)
                            ux - pitch? 0 is no pitch, -1 is down

            a - altitude of the aircraft in m
            vx, vy, vz - velocity of the aircraft (groundspeed I think) as a matrix
                            vz - + is up, - is down
                                    vx  vy
                            North - 0   +
                            East  - +   0
                            South - 0   -
                            West  - -   0
            wx, wy, wz - wind speed relative to the aircraft
        
    
    Aircraft Response Systems:
        Starting variables:
            Pitch 0
            Velocity 6
            Roll 0 (not implemented)
        Response to STALL (pitch > 0, vertical velocity < 0):
            NONE
        Response to too much speed (horizontal velocity > required):
            Required pitch +0.1
            Throttle -0.2
        Response to too little speed (horizontal velocity < required):
            Required pitch -0.1
            Throttle +0.2
        Response to roll:
            Roll opposite 0.2
        Response to high pitch (pitch > required):
            Pitch down by required pitch -0.01
        Response to low pitch (pitch < required):
            Pitch up by required pitch +0.01


"""

requiredPitch =             0   # pitch
requiredHVelocity =         6   # speed
requiredRoll =              0   # bank / roll
requiredAltitude =        100   # altitude above sea level

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


pause()
send("reset")

receiver = Receiver(sock, BUFSIZ)
receive_thread = Thread(target=receiver.receive)
receive_thread.start()

control()
send("control 0 0")
send("control 1 0")
send("control 2 0")
send("control 3 0")
resume()

# Custom code here
send("requesttelemetry 0.1")
#send("releasecontrol")

tel = {}
fixPitch = False
fixThrottle = False
control1 = 0
control3 = 0
i = 0
while True:
    tel = receiver.getTelemetry()
    if tel.get("faceDir") == None:
        print("Main thread: No data received.")
        sleep(0.5)
        continue
    alt = float(tel.get("pos")[2])
    pitch = float(tel.get("faceDir")[2])
    hvelocity = (float(tel.get("vel")[0]) ** 2 + float(tel.get("vel")[1]) ** 2) ** 0.5
    vvelocity = float(tel.get("vel")[2])
    roll = float(tel.get("upDir")[1])

    ####### STALL #######
    """if vvelocity < 1 and pitch > 0:
        if control3 > 0.9 and requiredPitch > -0.3:
            fixThrottle = True
            requiredPitch -= 0.1
            print("SP")
        if control3 <= 0.9:
            fixThrottle = True
            control3 += 0.3
            print("ST")"""

    ####### ALTITUDE #######
    relativeAlt = alt - requiredAltitude
    #print(relativeAlt)
    if abs(relativeAlt) > 0:
        fixPitch = True
        #fixThrottle = True
        if relativeAlt > 0 and pitch > -0.1:
            requiredPitch -= 0.04
            requiredHVelocity = 5
            #control3 -= 0.1
        elif relativeAlt < 0 and pitch < 0.1:
            requiredPitch += 0.04
            requiredHVelocity = 10
            #control3 += 0.1
    else:
        fixPitch = False

    ####### VELOCITY #######
    relativeHVelocity = hvelocity - requiredHVelocity
    if abs(relativeHVelocity) > 0:
        if relativeHVelocity > 0:
            if not fixThrottle:
                control3 = 0.2
            send("control 3 -%f" % control3)
            """if not fixPitch:
                requiredPitch += 0.01"""
            i += 1
        else:
            if not fixThrottle:
                control3 = 1# / (requiredHVelocity / relativeHVelocity)
            send("control 3 %f" % control3)
            """if not fixPitch:
                requiredPitch -= 0.01"""
            i += 1
    ####### PITCH #######
    relativePitch = pitch - requiredPitch
    if abs(relativePitch) > 0.01:
        control1 = abs(relativePitch) - 0.01
        if relativePitch > 0:
            send("control 1 %f" % control1)
            requiredHVelocity += 0.5
            i += 1
        else:
            send("control 1 -%f" % control1)
            requiredHVelocity -= 0.5
            i += 1
    ####### ROLL ########
    relativeRoll = roll - requiredRoll
    if abs(relativeRoll) > 0:
        if relativeRoll > 0:
            send("control 0 -%f" % 0.5)#(abs(relativeRoll)))
        else:
            send("control 0 %f" % 0.5)#(abs(relativeRoll)))
    fixPitch = False
    fixThrottle = False
    sleep(0.1)

# Custom code ends here

close(receiver)
print("Closed")
