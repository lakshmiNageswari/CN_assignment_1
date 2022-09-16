#!/usr/bin/env python3

import socket
import os
import tqdm
HOST =  socket.gethostname()  # The server's hostname or IP address
PORT = 65432  # The port used by the server

cmd=str(input())
command = cmd.split()


def decrypt(parameter,mode):
    
    mode=int(mode)
    lst=parameter.split()
    # print(lst)
    final=[]
    for j in range(len(lst)):
        data=lst[j]
        if mode==0: 
            final.append(data.decode())
        
        elif mode==1:
            s=""
            offset=2
            for r in data:
             
                p=chr(r)
             
                if p.isalpha():
                    s=s+chr(ord(p)-offset)
                    
                elif p.isdigit():
                    s=s+str(int(p)-offset)
                    
                else:
                    s=s+p
                    
            final.append(s)
            
        else:
            
            final.append(data[::-1].decode())
            
            
    return " ".join(final)




with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.send(cmd.encode())
    
    k=s.recv(1024).decode()
    while k:
       
    
        if command[0]=="UPD":
            s.send("testing".encode())
            filename=command[1]
            filename = os.path.basename(filename)
            print(filename)
            
            f = open(filename,'rb')
            l = f.read(1024)
            while (l):
                s.send(l)
                # print('Sent ',repr(l))
                l = f.read(1024)
            f.close()
            s.close()
            
            # print("file closed!")
            break 
        
        elif command[0]=="DWD":
            
            current=os.getcwd()
                
            with open('download_file', 'wb') as f:
                 
                    while True:
                        # print('receiving data...')
                        content = s.recv(1024)
                        # print(decrypt(content,command[2]))
                        # print(content)
                        
                        if not content:
                            break
                      
                        f.write(decrypt(content,command[2]).encode())
                    f.close()
                    
            print("file closed!")
            s.close()
            break
                    
       
            
        else:
            data = s.recv(1024).decode()
            print(data)
            s.close()
            break
        
    
