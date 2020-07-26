import socket
import threading
import re
from urllib import parse


def server_client(new_socket):
    """为这个客户端返回数据"""
    # 1.接收浏览器发过来的请求，即http请求
    request = new_socket.recv(1024).decode("utf-8")
    request = parse.unquote(request)  # 字符串解码
    #print(request)
    request_lines = request.splitlines()
    print(request_lines)
    file_name = ""
    ret = re.match(r"[^/]+(/[^ ]*)", request_lines[0])
    if ret:
        file_name = ret.group(1)
        if file_name == "/":
            file_name = "/index.html"
    try:
        f = open("D:\陈益光\练习" + file_name, "rb")
    except:
        response = "HTTP/1.1 404 NOT FOUND\r\n"
        response += "\r\n"
        response += "------file not found-----"
        new_socket.send(response.encode("utf-8"))
    else:
        file_content = f.read()
        f.close()
    # 2.发送http格式数据给浏览器
    # 2.1准备发给浏览器的数据----heard
        response = "HTTP/1.1 200 OK\r\n"
        response += "\r\n"
    # 2.2准备发给浏览器的数据----body
    # file = open("D:\陈益光\练习\index.html", "rb")
    # content = file.read()
    # file.close()
    # response += content
        new_socket.send(response.encode("utf-8"))
        new_socket.send(file_content)
        new_socket.close()


def main():
    # 创建套接字
    tcp_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 绑定IP和port
    tcp_server.bind(("", 8890))
    # 监听
    tcp_server.listen(128)
    while True:
        # 等待新客户的链接
        new_socket, client_address = tcp_server.accept()
        t1 = threading.Thread(target=server_client, args=(new_socket,))
        t1.start()
        # 为这个客户端服务
        #server_client(new_socket)
    tcp_server.close()


if __name__ == "__main__":
    main()