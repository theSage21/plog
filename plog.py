import socket
from multiprocessing import Queue
import time

server_address = ('127.0.0.1', 8989)
Q = Queue()  # Global queue for messages
QSIZE = 500 # things to hold in queue

def log(data, filename='plogfile.log'):
    """
    Write data to a file.
    """
    Q.put(str(data))
    if Q.qsize() > QSIZE:
        data = []
        for i in range(QSIZE):
            try:
                i = Q.get(block=False)
                data.append(i)
            except:
                break
        with open(filename, 'a') as fl:
            fl.write(''.join(data))


def listen(filename):
    """
    Listen for incoming data
    """
    global server_address, QSIZE
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print('starting up on %s port %s' % server_address)
    print('Buffer size of messages: {}'.format(QSIZE))

    sock.bind(server_address)
    sock.listen(QSIZE)
    count = 0

    last_print = time.time()
    while True:
        try:
            connection, client_address = sock.accept()
            data = connection.recv(1024).decode()
            log(data, filename)
            count += 1
            # PRINT IF ENOUGH TIME PASSES
            if time.time() - last_print > 5:
                print(count, 'logs completed')
                last_print = time.time()
        except KeyboardInterrupt:
            data = []
            while True:
                try:
                    i = Q.get(block=False)
                    data.append(i)
                except:
                    break
            with open(filename, 'a') as fl:
                fl.write(''.join(data))
            connection.close()
            break
            

def addlog(data):
    """
    Send data to logging service
    """
    assert isinstance(data, str)
    # TODO: add something to handle `unable to assign port`
    with socket.create_connection(server_address) as sock:
        sock.sendall(data.encode())



if __name__ == '__main__':
    import sys
    filename = sys.argv[1]
    print('Logging to: ', filename)
    listen(filename)
