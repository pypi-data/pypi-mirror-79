from socket import*
def login(user,password):
    try:
        s = socket(AF_INET, SOCK_STREAM)
        s.connect(("pan.asunc.cn",22001))
        s.send(user.encode("utf-8"))
        s.send(password.encode("utf-8"))
        print(s.recv(1).decode("utf-8"))
    except:
        raise Exception("连接服务器失败")