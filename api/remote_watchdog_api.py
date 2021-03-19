#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author: i2cy(i2cy@outlook.com)
# Filename: heartbeat_control_API
# Created on: 2020/9/17

import socket
import time
import threading
from i2cylib.utils.logger import *


KILL_COMMAND = "taskkill /IM 小栗子框架-快载.exe"
START_COMMADN = ".\\小栗子框架-快载.exe"


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


class heartbeatControl:
    def __init__(self, key=None, feedThreshold=30,
                 host="127.0.0.1", port=10430, log=None):
        if log is None:
            log = logger()
        self.logger = log
        self.serverAddr = (host, port)
        self.timeKey = key
        if self.timeKey == None:
            self.timeKeyClass = None
        else:
            self.timeKeyClass = timeKey(self.timeKey)
        self.feedTime = time.time()
        self.feedThreshold = feedThreshold
        self.qqAPI = None
        self.LIVE = True


    def _connect(self):
        try:
            clt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            clt.settimeout(3)
            clt.connect(self.serverAddr)
            clt.sendall(self.timeKeyClass.keygen())
            feedback = clt.recv(1024)
            if feedback == b"OK":
                return clt
            else:
                return "auth failed"
        except Exception as err:
            return str(err)


    def set_qqAPI(self, qqAPI):
        self.qqAPI = qqAPI


    def send_command(self, cmd):
        res = {"status":True, "ret":""}
        try:
            clt = self._connect()
            if type(clt) == type("string"):
                res["status"] = False
                res["ret"] = clt
                return res
            clt.sendall(cmd.encode())
            ret = clt.recv(1024)
            res["ret"] = ret
            clt.close()
        except Exception as err:
            clt.close()
            res["status"] = False
            res["ret"] = str(err)
        return res


    def restartQQframe(self):
        global KILL_COMMAND
        global START_COMMADN
        head = "[qqbotapi] [watchdog]"
        self.logger.WARNING("{} restarting QQ frame...".format(head))
        for i in range(3):
            res = self.send_command(KILL_COMMAND)
            time.sleep(1)
        self.logger.DEBUG("{} killing status: {}".format(head, res))
        time.sleep(1)
        res = self.send_command(START_COMMADN)
        self.logger.DEBUG("{} starting status: {}".format(head, res))
        self.logger.INFO("{} QQ frame restarted".format(head))
        time.sleep(10)
        self.logger.DEBUG("{} reallocating session...".format(head))
        self.qqAPI.sessionID = None
        try:
            sessionID = self.qqAPI.allocateSession()
            self.logger.INFO("{} allocated QQbot session ID: {}".format(head, str(sessionID)))
        except Exception as err:
            self.logger.ERROR("{} failed to allocate session, {}".format(head, err))


    def heartbeatLoop_thread(self):
        while self.LIVE:
            if time.time() - self.feedTime > self.feedThreshold:
                self.restartQQframe()
                self.feedTime = time.time() + self.feedThreshold / 4
            time.sleep(1)


    def startHeartbeat(self):
        th = threading.Thread(target=self.heartbeatLoop_thread)
        th.start()


    def stopHeartbeat(self):
        self.LIVE = False


    def feed(self):
        self.feedTime = time.time()