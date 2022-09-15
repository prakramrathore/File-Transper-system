# echo-server.py

from email import charset
import socket
import os
import funcz

HOST = socket.gethostname() # The server's hostname or IP address
PORT = 4040  # The port used by the server

def create_server(host, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    s.listen()
    return s

def upload(conn, cmd, encode):
    filename = cmd.split()[-1]
    file = open(os.path.join(os.getcwd(),filename), "w")

    while True:
        data = conn.recv(1024).decode("utf-8")
        data = funcz.format_msg_decode(data, encode)
        if not data:
            break
        file.write(data)
    file.close()

def download(conn, cmd, encode):
    filename = cmd.split()[1]
    file = open(os.path.join(os.getcwd(),filename),"r")
    while True:
        data = file.read(1024)
        if not data:
            file.close()
            break
        data = funcz.format_msg_encode(data, encode)
        conn.send(bytes(data, "utf-8"))


print("[+] Server started")
s = create_server(HOST, PORT)
print("[+] Server created")

while True:
    try:
        conn, addr = s.accept()
        print(f"[+] Connected to client at address {addr}")
        encode = conn.recv(1024).decode("utf-8")
        print(encode)
        while True:
            cmd = conn.recv(1024).decode('utf-8')
            if not cmd:
                break
            cmd = funcz.format_msg_decode(cmd, encode)
            print(f">>> command received {cmd}")
            if(cmd == 'cwd'):
                # print(os.getcwd())
                data = funcz.format_msg_encode(os.getcwd(), encode)
                conn.send(bytes(data, "utf-8"))
                conn.close()
                break
            elif(cmd == 'ls'):
                # conn.send(bytes(os.listdir(os.getcwd()), "utf-8"))
                ls = ""
                ls+="[ "
                for l in os.listdir(os.getcwd()):
                    ls+=l
                    ls+=", "
                ls+=" ]"
                ls = funcz.format_msg_encode(ls, encode)
                conn.send(bytes(ls,"utf-8"))
                conn.close()
                break
            elif(cmd[0:2] == "cd"):
                if(cmd[2:4] ==".."):
                    os.chdir("..")
                else:
                    os.chdir(os.getcwd() + "/" + cmd[3:])
                data = funcz.format_msg_encode(os.getcwd(), encode)
                conn.send(bytes(data, "utf-8"))
                conn.close()
                break
            elif(cmd[0:3]=="upd"):
                upload(conn, cmd, encode)
                conn.close()
                break
            elif(cmd[0:3]=="dwd"):
                download(conn, cmd, encode)
                conn.close()
                break
                
        conn.close()
    except (ConnectionError, BrokenPipeError):
        print("Socket error")
        break
s.close()
