import socket
from multiprocessing import Queue
import time

server_address = ('127.0.0.1', 8989)

Q = Queue()
def log(data, filename='plogfile.log'):
    Q.put(str(data))
    if Q.qsize() > 500:
        data = []
        for i in range(500):
            try:
                i = Q.get(block=False)
                data.append(i)
            except:
                break
        with open(filename, 'a') as fl:
            fl.write(''.join(data))


def listen(filename):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print('starting up on %s port %s' % server_address)

    sock.bind(server_address)
    sock.listen(500)
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
    # TODO: add something to handle `unable to assign port`
    with socket.create_connection(server_address) as sock:
        sock.sendall(data.encode())



if __name__ == '__main__':
    import sys
    filename = sys.argv[1]
    print('Logging to: ', filename)
    listen(filename)
