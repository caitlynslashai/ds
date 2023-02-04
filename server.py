import sys
import socket
# import selectors
# deprecated from non-concurrent implementation
import types
import re
from _thread import *
import threading
from random import random
from time import sleep

# constant declarations
STORAGE_FILE = "storage.txt"
PORT = 9889
IP = "127.0.0.1"

storage = {}

print_lock = threading.Lock()

def load_from_storage():
    # loads all key/value sets from the storage file
    # saves key/value sets as lists
    storage = {}
    with open(STORAGE_FILE, "r") as f:
        lines = f.readlines()
        for line in lines:
            if(line==''):
                break
            parts = line.strip().split(" ")
            key = parts[0]
            valsize = int(parts[1])
            value = " ".join(parts[2:])
            storage[key] = (valsize, value)
        f.close()

    return storage

def save_to_storage(key, valsize, value):
    # saves a key, valuesize, value to the storage file
    # designed to work with load_from_storage()
    with open(STORAGE_FILE, "a") as f:
        f.write(f"{key} {valsize} {value}\n")
        f.close()

def reset_storage(storage):
    # resets the storage txt file so it only has the current value for each key
    with open(STORAGE_FILE, "w") as f:
        for key in storage:
            item = storage[key]
            print(key)
            print(item)
            f.write(f"{key} {item[0]} {item[1]}\n")

def get(key, storage):
    # returns key/valuesize/value triad from the storage dictiomary
    out = "END\r\n"
    if key in storage:
        item = storage[key]
        out = f"VALUE {key} {item[0]}\r\n{item[1]}\r\n" + out
    return out

def set(key, valuesize, value):
     try:
        storage[key] = (valuesize, value)
        save_to_storage(key, valuesize, value)
        return "STORED\r\n"
     except Exception as e:
        return "NOT STORED\r\n"

def command_thread(c, data, flag, stored):
    command = data.decode('utf-8').replace('\r','').split('\n')
    for line in command:
        line = line + "\n"
        print(repr(line))
        if flag == "set":
          #  try:
                print(stored)
                return {'flag':None, 'stored':None, 'out':set(stored['key'], stored['valsize'], line[:-1])}
          #  except Exception as e:
              #  return {'flag':None, 'stored':None, 'out':'NOT STORED\r\n'}
        elif re.match('get[ ]+[^ ]+\n', line):
          #  try:
                key = line.split(' ')[1]
                return {'flag':None, 'stored':None, 'out':get(key[:-1], storage)}
          # except Exception as e:
              #  return {'flag':None, 'stored':None, 'out':'ERROR\r\n'}
        elif re.match('^get \n', line):
            return{'flag':None, 'stored':None, 'out':'incorrect arguments for get\r\n'}
        elif re.match('set[ ]+[^ ]+[ ]+[^ ]+\n', line):
            try:
                split = line.split(' ')
                key = split[1]
                valsize = split[2][:-1]
                if not valsize.isdigit():
                    print(repr(valsize))
                    return {'flag':None, 'stored':None, 'out':'VALSIZE should be an integer\r\n'}
                flag = 'set'
                stored = {'key':key, 'valsize':valsize}
            except Exception as e:
                return {'flag':None, 'stored':None, 'out':'ERROR\r\n'}
        elif re.match('set .*\n', line):
            return{'flag':None, 'stored':None, 'out':'incorrect arguments for set\r\n'}
        else:
            return {'flag':None, 'stored':None, 'out':'INVALID COMMAND\r\n'}
    return {'flag':flag, 'stored':stored, 'out':'\r\n'}

                


def connection_thread(c):
    try:
        flag = None
        stored = None
        while True:
            valsize = 1024
            if stored:
                valsize = int(stored['valsize'])

            data = c.recv(valsize)
            if not data:
                print('Client disconnected')

                # print_lock.release()
                break
            else:
                print_lock.acquire()
                sleep(random()/10)

                results = command_thread(c, data, flag, stored)

                flag = results['flag']
                stored = results['stored']
                out = results['out']

                c.send(out.encode())

                print_lock.release()
    except KeyboardInterrupt:
        print("Exiting connection thread due to KeyboardInterrupt")
    finally:
        c.close()

if __name__ == '__main__':
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((IP, PORT))
    s.listen()
    print(f"Listening on {(IP, PORT)}")
    # s.setblocking(False)

    # load dictionary from persistent storage
    storage = load_from_storage()

    # clean persistent storage file
    reset_storage(storage)

    print(storage)
    try:
        while True:
            c, addr = s.accept()

            # print_lock.acquire()
            print('Connected to:', addr[0], ':', addr[1])

            start_new_thread(connection_thread, (c,))
    except KeyboardInterrupt:
        print("caught KeyboardInterrupt, exiting")
    finally:
        s.close()



