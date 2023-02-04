import socket
import threading
import sys
from _thread import *
from threading import *

print_lock = Lock()

def connect_thread(ide, sem, sem2):
    # local host IP '127.0.0.1'
    host = '127.0.0.1'
 
    # Define the port on which you want to connect
    port = 9889
    
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
 
    # connect to server on local computer
    s.connect((host, port)) 

    i = 0
    try:
        i = int(sys.argv[2])
    except IndexError:
        pass
    
    for j in range(i):
        print_lock.acquire()
        s.send(f"set a 1024\r\n{str(ide)}\r\n".encode('ascii'))
        s.recv(1024)
        s.send("get a\r\n".encode('ascii'))
        print(s.recv(1024).decode('ascii'))
        print_lock.release()

    sem.release()
    sem2.acquire()
    print("test\n")
    # close the connection
    s.close()

 
if __name__ == '__main__':
    threads = []
    sem = Semaphore(0)
    sem2 = Semaphore(0)
    for i in range(int(sys.argv[1])):
        t = Thread(target=connect_thread, args=(i, sem, sem2))
        threads.append(t)
    for t in threads:
        t.start()
    for t in threads:
        sem.acquire()
    for t in threads:
        sem2.release()
        

