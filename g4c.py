import socket
 
 
def Main():
    # local host IP '127.0.0.1'
    host = '127.0.0.1'
 
    # Define the port on which you want to connect
    port = 9889
 
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
 
    # connect to server on local computer
    s.connect((host,port))
 
    while True:
        message = input('Type the message to send to server or type \'exit\' to exit\n')
        if message == 'exit':
            break

        # message sent to server
        s.send(message.encode('ascii'))
 
        # message received from server
        data = s.recv(1024)
 
        # print the received message
        # here it would be a reverse of sent message
        print('Received from the server :',str(data.decode('ascii')))
 
    # close the connection
    s.close()
 
if __name__ == '__main__':
    Main()
