

import socket
import os
import tqdm
HOST = socket.gethostname()  
PORT = 65432 

def encrypt(parameter,mode):
    
    mode=int(mode)
    lst=parameter.split()
 
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
                    s=s+chr(ord(p)+offset)
                    
                elif p.isdigit():
                    s=s+str(int(p)+offset)
                    
                else:
                    s=s+p
                    
            final.append(s)
            
        else:
            
            final.append(data[::-1].decode())
            
            
    return " ".join(final)


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        # while True:
            print(f"Connected by {addr}")
            data = conn.recv(1024).decode()
            data = data.split(' ')
         
            conn.send("Arguments are received!".encode())
          
            if data[0]=="CWD":
                conn.send(os.getcwd().encode())
            elif data[0]=="LS":
                files = [f for f in os.listdir('.') if os.path.isfile(f)]
                files=str(files)
                conn.send(files.encode())
            elif data[0]=="CD":
                os.chdir(data[1])
                conn.send(os.getcwd().encode())
                
            elif data[0]=="UPD":
      
                receiving=conn.recv(1024).decode()
               
                with open('uploaded_file', 'wb') as f:
                    
                    while True:
                        # print('receiving data...')
                        content = conn.recv(1024)
                     
                        if not content:
                            break
                    
                        # print(content)
                        f.write(content)
                    f.close()
          
                        
            elif data[0]=="DWD":
                filename=data[1]
               
                
                f = open(filename,'rb')
                l = f.read(1024)
                while (l):
                    print(str(l))
                    encrypted = encrypt(l,data[2]).encode()
                 
                    conn.send(encrypted)
                   
                    l = f.read(1024)
                f.close()
                        
            else:
                print("no proper input")
                
            conn.close()
                
                
               
                

                
  
                
