import time
from threading import Thread
from client import receive_loop
from server import send_loop

if __name__ == '__main__':
    cloud_server_thread = Thread(target=send_loop, args=("cloud", ))
    cloud_client_thread = Thread(target=receive_loop, args=("cloud", ))

    cloud_server_thread.start()
    time.sleep(5)
    cloud_client_thread.start()