import socket
import sys
import time
import errno
from multiprocessing import Process

def process_start(s_sock):
    content = s_sock.recv(32)
    s_sock.send(ok_message)
    s_sock.close()
    #time.sleep(10)
    sys.exit(0) # kill the child process

if __name__ == '__main__':
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((sys.argv[1], int(sys.argv[2])))
    print 'listen on address %s and port %d' % (sys.argv[1], int(sys.argv[2]))
    s.listen(1)
    try:
        while True:
            try:
                s_sock, s_addr = s.accept()
                p = Process(target=process_start, args=(s_sock,))
                p.start()

            except socket.error:
                # stop the client disconnect from killing us
                print 'got a socket error'

    except Exception as e:
        print 'an exception occurred!',
        print e
        sys.exit(1)
    finally:
        s.close()