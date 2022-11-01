from concurrent.futures import ThreadPoolExecutor
import socket

class Client:
    def __init__(self, port) -> None:
        self.ip = ''
        self.port = port
        self.buf = 1024

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((self.ip, self.port))

    def thr(self):
        data = self.sock.recv(self.buf)
        self.dat = data.decode(encoding='utf-8')
        return self.dat

if __name__ == '__main__':
    pool = ThreadPoolExecutor(max_workers=2, thread_name_prefix='thread')

    c1 = Client(8888)
    s1 = []

    c2 = Client(9999)
    s2 = []

    c3 = Client(7777)
    s3 = []

    while True:
        try:
            s1.append(pool.submit(c1.thr))
            d1 = s1[-1].result()

            s2.append(pool.submit(c2.thr))
            d2 = s2[-1].result()

            s3.append(pool.submit(c3.thr))
            d3 = s3[-1].result()

            print(d1, d2, d3)
            
        except:
            break