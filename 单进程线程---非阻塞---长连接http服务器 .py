import socket
import threading
import re, time
from urllib import parse


def server_client(new_socket, request):
    """为这个客户端返回数据"""
    request = parse.unquote(request)  # 字符串解码
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
        response_body = "------file not found-----"
        response_header = "HTTP/1.1 404 NOT FOUND\r\n"
        response_header += "Content-Length:%d\r\n" % len(response_body)
        response_header += "\r\n"

        response = response_header.encode("utf8") + response_body.encode("utf8")
        new_socket.send(response)
    else:
        file_content = f.read()
        f.close()
        response_body = file_content
        response_header = "HTTP/1.1 200 OK\r\n"
        response_header += "Content-Length:%d\r\n" % len(response_body)
        response_header += "\r\n"

        response = response_header.encode("utf8")+response_body
        new_socket.send(response)


def main():
    # 创建套接字
    tcp_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 绑定IP和port
    tcp_server.bind(("", 8890))
    # 监听
    tcp_server.listen(128)
    tcp_server.setblocking(False)  # 把套接字设置非堵塞
    cli_socket_list = []
    while True:
        time.sleep(0.5)
        try:
            new_socket, client_address = tcp_server.accept()   # 等待新客户的链接
        except Exception as e:
            print("没有新的客户端到来")
        else:
            new_socket.setblocking(False)      # 把套接字设置非堵塞
            cli_socket_list.append(new_socket)  # 把新的客户端添加到列表
            print("有新的客户端到来")

        for new_socket in cli_socket_list:
            try:
                rec_data = new_socket.recv(1024).decode("utf8")
            except Exception as e:
                print("这个客户端没有发送数据")
                # print(e)
            else:
                print(rec_data)
                if rec_data:
                    print("客户端发送了数据")
                    server_client(new_socket, rec_data)

                else:
                    new_socket.close()
                    cli_socket_list.remove(new_socket)

                    print("客户端关闭了连接")


if __name__ == "__main__":
    main()