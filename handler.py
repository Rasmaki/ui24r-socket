import os, sys, threading
import time
import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    client.connect(('192.168.1.48', 80))
except socket.error:
    print('Connection failed.')
    sys.exit(1)
client.send(bytes('GET /raw HTTP1.1\n\n', 'utf-8'))

data = client.recv(1024)
print("Started")
fader = ""
old = -1
mute = -1

try:
    while True:
        client.send(bytes("ALIVE\n", 'utf-8'))
        data = client.recv(128)
        lines = data.split(bytes("\n", 'utf-8'))
        # client.send(bytes('SETD^i.0.mute^0\n', 'utf-8'))
        for line in lines:
            if bytes('SETD^i.0.mix', 'utf-8') in line:
                if line != fader:
                    fader = line
                    number = fader.replace(bytes('SETD^i.0.mix^', 'utf-8'), bytes('', 'utf-8'))
                    try:
                        number = float(number.decode('utf-8'))
                        print(str(int(number*100)) + '%')
                    except Exception as e:
                        client.send(bytes("ALIVE\n", 'utf-8'))
        for line in lines:
            if bytes('SETD^i.0.mute^0', 'utf-8') in line:
                mute = 0
                client.send(bytes("ALIVE\n", 'utf-8'))
            elif bytes('SETD^i.0.mute^1', 'utf-8') in line:
                mute = 1
                client.send(bytes("ALIVE\n", 'utf-8'))
        if old != mute:
            if mute == 0:
                print("Unmuted")
                old = mute
            elif mute == 1:
                print("Muted")
                old = mute
except KeyboardInterrupt:
    exit()
client.close()
print("Disconnected")
