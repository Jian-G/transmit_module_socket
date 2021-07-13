import socket,os,hashlib
import core
import glob
import json
import struct
from threading import Thread
model_dict = {}
param_dict = {}
tensor_dict = {}

def send_loop(type):
    if type == 'cloud':
        server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        server.bind(core.CLOUD_HOST, core.CLOUD_SENTTO_EDGE)
        server.listen(5)
        # count = 0
        while True:
            conn, addr = server.accept()
            # count += 1
            print("Cloud Server(I) {} : {} has connected to Edge client(others) {} : {}".
                  format(core.CLOUD_HOST),core.CLOUD_SENTTO_EDGE,addr[0],addr[1])
            while True:
                for filename in glob.glob(r'data/send/model/*.pt'):
                    if(filename not in model_dict.keys()):
                        model_dict[filename] = 0
                for filename, status in model_dict.items():
                    if status == 0:
                        send_file(conn, filename)
    if type == 'edge':
        server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        server.bind(core.EDGE_HOST, core.EDGE_SENDTO_CLOUD)
        server.listen(5)
        # count = 0
        while True:
            conn, addr = server.accept()
            # count += 1
            print("Edge Server(I) {} : {} has connected to Cloud client(others) {} : {}".
                  format(core.CLOUD_HOST),core.CLOUD_SENTTO_EDGE,addr[0],addr[1])
            while True:
                for filename in glob.glob(r'data/send/model/*.txt'):
                    if(filename not in tensor_dict.keys()):
                        tensor_dict[filename] = 0
                for filename, status in tensor_dict.items():
                    if status == 0:
                        send_file(conn, filename)    


def send_file(conn, filename):
    filesize = os.path.getsize(filename)
    dict = {
        'filename': filename,
        'filesize': filesize,
    }
    head_info = json.dumps(dict)
    head_info_len = struct.pack('i', len(head_info))
    # 发送头部长度
    conn.send(head_info_len)
    # 发送头部信息
    conn.send(head_info.encode('utf-8'))
    with open(filename, 'rb') as f:
        # 16进制摘要
        m = hashlib.md5()
        data = f.read()
        # 发送文件
        conn.sendall(data)
        # 核验文件
        m.update(data)
        conn.send(m.hexdigest().encode())
    print("File {} ({} MB) send finish.".format(filename, filesize/1024/1024))

if __name__ == '__main__':
    edge_server = Thread(target=send_loop, args=("cloud", ))
    