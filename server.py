import socket,os
from time import time
import core
import glob
import json
import struct
from threading import Thread
from load_model import edge_load_model
model_dict = []
param_dict = []
tensor_dict = []

def send_loop(type):
    if type == 'cloud':
        server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        server.bind((core.CLOUD_HOST, core.CLOUD_SENTTO_EDGE))
        server.listen(5)
        while True:
            conn, addr = server.accept()
            print("Cloud Server(I) {} : {} has connected to Edge client(others) {} : {}".
                  format(core.CLOUD_HOST,core.CLOUD_SENTTO_EDGE,addr[0],addr[1]))
            while True:
                # 发送pdmodel文件
                for filename in glob.glob(r'data/send/model/client_infer_*.pdmodel'):
                    if(filename not in model_dict):
                        model_dict.append(filename)
                        send_file(conn, filename)
                # 发送pdiparams文件
                for filename in glob.glob(r'data/send/model/client_infer_*.pdiparams'):
                    if(filename not in param_dict):
                        param_dict.append(filename)
                        send_file(conn, filename)

    if type == 'edge':
        server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        server.bind((core.EDGE_HOST, core.EDGE_SENDTO_CLOUD))
        server.listen(5)
        while True:
            conn, addr = server.accept()
            print("Edge Server(I) {} : {} has connected to Cloud client(others) {} : {}".
                  format(core.EDGE_HOST,core.EDGE_SENDTO_CLOUD,addr[0],addr[1]))
            index = 0
            while True:
                tensor = edge_load_model(path_prefix="./data/receive/model/client_infer_resnet18_cifar10")
                send_tensor(conn, tensor, index)
                index += 1
                time.sleep(10)
                # for filename in glob.glob(r'data/send/tensor/*.txt'):
                #     if(filename not in tensor_dict):
                #         tensor_dict.append(filename)
                #         send_file(conn, filename)


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
        # 发送文件信息
        data = f.read()
        conn.sendall(data)
    print("\nFile {} ({} MB) send finish.".format(filename, round(filesize/1000/1000,2)))

def send_tensor(conn, tensor, name):
    tensorsize = os.path.getsize(tensor)
    dict = {
        'filename': name,
        'filesize': tensorsize,
    }
    head_info = json.dumps(dict)
    head_info_len = struct.pack('i', len(head_info))
    # 发送头部长度
    conn.send(head_info_len)
    # 发送头部信息
    conn.send(head_info.encode('utf-8'))
    conn.send(tensor)
    print("\nFile {} ({} MB) send finish.".format(name, round(tensor/1000/1000,2)))


if __name__ == '__main__':
    edge_server = Thread(target=send_loop, args=("cloud", ))
    