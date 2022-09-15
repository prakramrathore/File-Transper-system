# echo-client.py

import socket
import os
import funcz

HOST = socket.gethostname()  # The server's hostname or IP address
PORT = 4040  # The port used by the server


def upload(s, cmd, encode):

    file = open(cmd[4:],"r")
    while True:
        data = file.read(1024)
        if not data:
            file.close()
            break
        data = funcz.format_msg_encode(data, encode)
        s.send(bytes(data, "utf-8"))

def download(s, cmd, encode):
    
    filename = cmd.split()[-1]
    file = open(os.path.join(os.getcwd(),filename), "w")

    while True:
        data = s.recv(1024).decode("utf-8")
        data = funcz.format_msg_decode(data, encode)
        if not data:
            break
        file.write(data)
    file.close()


if __name__ == "__main__":
    print("[+] Client Started")
    print("Enter the prefered format of encoding:\n Press 0 for Plain text \n Press 1 for Caeser cipher with offset 2 \n Press 2 for reverse encoding")
    encode = input()
    try:
        while True:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((HOST, PORT))
            # print("[+] Connected to server")
            s.send(bytes(encode,"utf-8"))
            cmd = input(">>> ")
            data = funcz.format_msg_encode(cmd, encode)
            s.sendall(bytes(data, 'utf-8'))
            if(cmd=="cwd"):
                data = s.recv(1024).decode("utf-8")
                print(funcz.format_msg_decode(data, encode))
                s.close()
            elif(cmd=="ls"):
                data = s.recv(1024).decode("utf-8")
                print(funcz.format_msg_decode(data, encode))
                s.close()
            elif(cmd[0:2]=="cd"):
                data = s.recv(1024).decode("utf-8")
                print(funcz.format_msg_decode(data, encode))
                s.close()
            elif(cmd[0:3]=="upd"):
                upload(s, cmd, encode)
                s.close()
                # print("[+] Server closed")
            elif (cmd[0:3]=="dwd"):
                download(s, cmd, encode)
                s.close()
                # print("[+] Server closed")
            elif(cmd=='q'):
                break
    except ConnectionError:
        print("Connection error")
    finally:
        s.close()
        print("Connection closed")
        print("[+] Server closed")
