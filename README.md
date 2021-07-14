# transmit_module_socket
**基于Socket的通信模块**
## 文件说明

- client.py：客户端接收文件，对于云接收tensor，对于端接收分割模型；
- server.py：服务端发送文件，对于云发送分割模型，对于端发送tensor；
- cloud.py：启动云的发送和接收线程；
- edge.py：启动端的发送和接收线程；
- core.py：常量定义，包括host、port、buffersize等内容
- data：数据存放文件夹（其中模型暂存为.pt文件，tensor暂存为.txt文件）
    - send：发送文件夹
        - model：云要发送的切割模型
        - tensor：端要发送的tensor特征
    - receive：接收文件夹
        - model：端接收到的切割模型
        - tensor：云接收到的tensor特征

## 启动方式

```bash
# 云线程
$ python3 cloud.py --cloud_host "xxx.xxx.xxx.xxx" --edge_host "xxx.xxx.xxx.xxx" --cloud_port n --edge_port n 

# 端线程
$ python3 edge.py --cloud_host "xxx.xxx.xxx.xxx" --edge_host "xxx.xxx.xxx.xxx" --cloud_port n --edge_port n 
```

Tips

1. host为必须项，port为可选项，默认为：8080（CLOUD_SENDTO_EDGE）和8081（EDGE_SENDTO_CLOUD）。
2. 云和端的启动参数应相同。**启动间隔小于5s。**
3. 接收和发送文件说明：模型包括.pdmodel模型架构和.pdparams模型参数两个文件，特征为.pdtensor文件。