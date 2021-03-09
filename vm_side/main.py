#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author: i2cy(i2cy@outlook.com)
# Filename: remote_controller
# Created on: 2020/9/17

"""
WARNING: INTERNAL NETWORK USE ONLY, UNENCRYPTED CONNECTION
WARNING: INTERNAL NETWORK USE ONLY, UNENCRYPTED CONNECTION
WARNING: INTERNAL NETWORK USE ONLY, UNENCRYPTED CONNECTION
"""

import socket
import time
import os
import threading


LISTENING_PORT = 10430
KEY = "__BasiCABCKey."


LIVE = True


class timeKey: # 64-Bits Live key generator/matcher
    def __init__(self,key):
        if type(key) != type(""):
            raise Exception("key must be a string")
        self.key = key
    def keygen(self,mt=0): # 64-Bits Live key generator
        dt = int(str(int(time.time()))[:-2]) + mt
        sub_key_unit = str(int(str(4*dt**8 + 8*dt**4 + 2*dt**2 + 4*dt + 1024)[::-1]) + 3*dt**4 + 2*dt**3 + 3*dt**2 + 2*dt)
        final_key = b""
        n = 0
        n2 = 0
        for i in range(64):
            if n == len(sub_key_unit):
                n = 0
            if n2 == len(self.key):
                n2 = 0
            final_key_unit = ord(self.key[n2]) + ord(sub_key_unit[n])
            if final_key_unit >= 255:
                final_key_unit -= 256
            final_key += bytes((final_key_unit,))
            n += 1
            n2 += 1
        return final_key
    def keymatch(self,key): # Live key matcher
        lock_1 = self.keygen(-1)
        lock_2 = self.keygen(0)
        lock_3 = self.keygen(1)
        lock = [lock_1,lock_2,lock_3]
        if key in lock:
            return True
        else:
            return False


def executer(cmd):
    try:
        pipe = os.popen(cmd)
        time.sleep(0.5)
        res = pipe.read()
    except Exception as err:
        res = str(err)
    print("execution result:", res)


def handler(con):
    try:
        con.settimeout(3)
        tk = timeKey(KEY)
        match = tk.keymatch(con.recv(1024))
        if not match:
            return
        else:
            con.sendall(b"OK")
        cmd = con.recv(2048).decode()
        thr = threading.Thread(target=executer, args=(cmd,))
        thr.start()
        con.sendall(b"OK")
        con.close()
    except Exception as err:
        try:
            con.sendall(str(err).encode())
            con.close()
        except:
            pass
        print("error while communicating with client,", err)


def listening_loop():
    global LIVE
    try:
        srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        srv.bind(("0.0.0.0", LISTENING_PORT))
        print("server bind at 0.0.0.0:{}".format(LISTENING_PORT))
        srv.settimeout(5)
        srv.listen(10)
    except Exception as err:
        print("failed to initialize server, {}, exiting".format(err))
        LIVE = False
        return
    while LIVE:
        try:
            con, addr = srv.accept()
            print("connection from {} in coming".format(str(addr)))
            handler_thread = threading.Thread(target=handler, args=(con,))
            handler_thread.start()
        except:
            continue
    srv.close()


def main():
    global LIVE
    print("initializing...")
    lis_thread = threading.Thread(target=listening_loop)
    lis_thread.start()
    print('(use Ctrl+C to exit)\n')
    while LIVE:
        try:
            time.sleep(2)
        except KeyboardInterrupt:
            LIVE = False
            exit(0)


if __name__ == "__main__":
    main()