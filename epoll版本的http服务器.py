import socket
import select
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

    # 创建epoll对象（用户进程与内核共享内存区）
    epl = select.epoll()
    # 将监听套接字对应的fd注册到epoll中
    epl.register(tcp_server.fileno(), select.EPOLLIN)

    fd_event_dict = dict()
    while True:
        fd_event_list = epl.poll()  # 默认堵塞，直到os监测到数据来 通过时间通知方式告诉这个程序，此时才会解堵塞
        for fd, event in fd_event_list:   # [(fd1,event),(fd2,event)]
            if fd == tcp_server.fileno():
                new_socket, client_address = tcp_server.accept()   # 等待新客户的链接
                epl.register(new_socket.fileno(), select.EPOLLIN)
                fd_event_dict[new_socket.fileno()] = new_socket
            elif event == select.EPOLLIN:
                rec_data = fd_event_dict[fd].recv(1024).decode("utf8")

                if rec_data:
                    print("客户端发送了数据")
                    server_client(fd_event_dict[fd], rec_data)
                else:
                    fd_event_dict[fd].close()
                    epl.unregister(fd)
                    del fd_event_dict[fd]
                    print("客户端关闭了连接")


if __name__ == "__main__":
    main()