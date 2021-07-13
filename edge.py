import time
from threading import Thread
from client import receive_loop
from server import send_loop

if __name__ == '__main__':
    edge_server_thread = Thread(target=send_loop, args=("edge", ))
    edge_client_thread = Thread(target=receive_loop, args=("edge", ))

    edge_server_thread.start()
    time.sleep(5)
    edge_client_thread.start()