import socket
import difflib
 
def Main():
    # local host IP '127.0.0.1'
    host = '127.0.0.1'
 
    # Define the port on which you want to connect
    port = 9889
 
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
 
    # connect to server on local computer
    s.connect((host,port))
 
    tests = []
    
    # test invalid value size
    tests.append(["set a onethousandtwentyfour\r\n", "VALSIZE should be an integer\r\n"])

    # test incorrect number of get arguments
    tests.append(["get a b\r\n", "INVALID COMMAND\r\n"])

    # test valid set command
    tests.append(["set testkey 1024\r\n", " "])
    tests.append(["the value of testkey is testvalue\r\n", "STORED\r\n"])

    # test insufficient set arguments
    tests.append(["set testkey\r\n", "incorrect arguments for set\r\n"])

    # test valid get command
    tests.append(["get testkey\r\n", "VALUE testkey 1024\r\nthe value of testkey is testvalue\r\nEND\r\n"])
    
    # test valid get command with no key found
    tests.append(["get testkeyfail\r\n", "END\r\n"])

    # test too many set arguments
    tests.append(["set toomanyargs 1024 test\r\n", "incorrect arguments for set\r\n"])

    for testc in tests:
        message = testc[0]
        # message sent to server
        s.send(message.encode('ascii'))
 
        # message received from server
        data = s.recv(1024)
 
        # decode the test case and assert that it matches
        rec = str(data.decode('ascii'))
        try:
            assert rec == testc[1]
        except AssertionError:
            print("Command :" + testc[0])
            print("Expected: " + testc[1])
            print("Actual: " + rec)
            
            for i,s in enumerate(difflib.ndiff(testc[1], rec)):
                if s[0]==' ': continue
                elif s[0] == '-':
                    print(u'Delete "{}" from position {}'.format(s[-1], i))
                elif s[0]=='+':
                    print(u'Delete "{}" from position {}'.format(s[-1],i))
            raise(AssertionError)
 
    # close the connection
    s.close()
 
if __name__ == '__main__':
    Main()
