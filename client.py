import json
import socket,hashlib
import struct
import core
import json
import time
from processbar import process_bar

def receive_loop(type):
    if type == "cloud":
        client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        client.connect((core.EDGE_HOST, core.EDGE_SENDTO_CLOUD))
    elif type == "edge":
        client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        client.connect((core.CLOUD_HOST, core.CLOUD_SENTTO_EDGE))
    while True:
        recv_file(client)

def recv_file(client):
    # 解析头部长度
    head_struct = client.recv(4)
    head_len = struct.unpack('i', head_struct)[0]
    # 解析文件信息
    file_info = client.recv(head_len)
    file_info = json.loads(file_info.decode('utf-8'))
    filesize = file_info['filesize']
    filename = file_info['filename']

    # 接收文件
    recv_len = 0
    start_time = time.time()
    filename = filename.replace("send", "receive")
    with open(filename, 'wb') as f:
        while recv_len < filesize:
            precent = recv_len / filesize
            process_bar(precent)
            md5 = hashlib.md5()
            if(filesize - recv_len > core.BUFFER_SIZE):
                recv_msg = client.recv(core.BUFFER_SIZE)
                f.write(recv_msg)
                recv_len += len(recv_msg)
            else:
                recv_msg = client.recv(filesize - recv_len)
                recv_len += len(recv_msg)
                f.write(recv_msg)
                print(recv_msg)
            md5.update(recv_msg)            
        md5_recv = client.recv(1024)
        if md5.hexdigest() == md5_recv.decode():
            print("File {} ({} MB) received correctly.".format(filename, filesize/1024/1024))
        else:
            print("File {} receive failed.".format(filename))
