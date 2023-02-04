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
    
    sockets = []

    q = 10
    try:
        q = int(sys.argv[2])
    except IndexError:
        pass

    i = 0
    try:
        i = int(sys.argv[3])
    except IndexError:
        pass
	    
    for i in range(q):
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        sockets.append(s)

    for s in sockets:
        # connect to server on local computer
        s.connect((host, port)) 

    for s in sockets:  
        for j in range(i):
        	s.send(f"set a 1024\r\n{str(ide)}\r\n".encode('ascii'))
        	s.recv(1024)
        	s.send("get a\r\n".encode('ascii'))
        	print(s.recv(1024).decode('ascii'))

    sem.release()
    sem2.acquire()
    print("test\n")
    # close the connection
    for s in sockets:
    	s.close()

 
if __name__ == '__main__':
    threads = []
    sem = Semaphore(0)
    sem2 = Semaphore(0)
    numclients = 100
    try:
        numclients = int(sys.argv[1])
    except IndexError:
        pass
    for i in range(numclients):
        t = Thread(target=connect_thread, args=(i, sem, sem2))
        threads.append(t)
    for t in threads:
        t.start()
    for t in threads:
        sem.acquire()
    for t in threads:
        sem2.release()
        

