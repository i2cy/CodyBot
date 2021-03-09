#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author: i2cy(i2cy@outlook.com)
# Filename: QQAPI_Cody
# Created on: 2020/9/13

import http.client as hclt
import json
import urllib.request as request
import urllib.parse as parse
import os
from api.remote_watchdog_api import *

global Cody

class CodyAPI:
    def __init__(self, configFile="Cody_QQ.json", heartbeatClass=None):
        config = json.loads(open(configFile,"rb").read())
        self.url = config["URL"]
        self.id = config["ID"]
        self.qqid = config["QQID"]
        self.nice = config["Nick"]
        self.managingGroups = config["ManagingGroups"]
        self.sessionID = None

        heartbeatClass.serverAddr = (config["HeartbeatHost"],
                                     config["HeartbeatPort"])
        heartbeatClass.timeKey = config["TimeKey"]
        heartbeatClass.feedThreshold = config["QQframeRestartThreshold"]

        heartbeatClass.timeKeyClass = timeKey(heartbeatClass.timeKey)

        heartbeatClass.set_qqAPI(self)

        self.heartbeatClass = heartbeatClass


    def mute(self, uin, mutetime, group):
        con = hclt.HTTPConnection(self.url, timeout=5)
        con.request('POST', '/mutegroupmember',
                    body="fromqq={}&group={}&toqq={}&time={}".format(
                        self.qqid,
                        group,
                        uin,
                        str(mutetime)
                    ))
        res = con.getresponse().read()
        return res


    def allocateSession(self):
        if self.sessionID != None:
            return self.sessionID
        con = hclt.HTTPConnection(self.url, timeout=5)
        con.request('POST', '/allocsession')
        res = con.getresponse().read()
        self.sessionID = str(json.loads(res)["session_id"])
        return self.sessionID


    def removeSession(self, sessionID=-1):
        if sessionID == -1:
            sessionID = self.sessionID
        try:
            con = hclt.HTTPConnection(self.url, timeout=5)
            con.request('POST', '/removesession',
                        "sessid={}".format(str(sessionID)))
            res = con.getresponse().read()
        except Exception as err:
            print("error while requesting to remove session,", err)
        self.sessionID = None
        return res


    def getEvent(self):
        if self.sessionID == None:
            return None
        con = hclt.HTTPConnection(self.url, timeout=5)
        con.request('POST', '/geteventv2',
                    "sessid={}".format(self.sessionID))
        res = con.getresponse().read()
        try:
            res = json.loads(res)
            res = res["events"]
            self.heartbeatClass.feed()
        except Exception:
            print("failed to decode events: {}".format(res))
            res = []
        return res


    def getPicUrl(self, picData, group):
        pics = []
        ret = []
        offset = 0
        index = 0
        while True:
            hashValue = ""
            offset = picData.find("[pic,hash=")
            if offset == -1:
                break
            else:
                pics.append("")
            ishash = False
            for i in picData[offset:]:
                pics[index] += i
                if i == "]":
                    break
                if ishash:
                    hashValue += i
                if i == "=":
                    ishash = True
            picData = picData[offset+len(pics[index]):]

            con = hclt.HTTPConnection(self.url, timeout=5)
            con.request('POST', '/getphotourl',
                        "photo={}&fromqq={}&group={}".format(
                            pics[index],
                            self.qqid,
                            group
                        ))
            res = con.getresponse().read()
            res = json.loads(res)["ret"]
            ret.append({"url": res, "hash": hashValue})
            index += 1

        return ret


    def downloadPic(self, url, filename):  # filename不包含文件后缀
        data = request.urlopen(url)
        contentType = data.headers.get("Content-Type")
        if contentType == None:
            return None
        contentType = contentType.split("/")
        if contentType[0] != "image":
            return None
        fileSize = int(data.headers.get("Size"))
        imageFile = open("{}.{}".format(filename, contentType[1]), "wb")
        wrote = 0
        while True:
            img = data.read(2048)
            if img == b"":
                break
            wrote += imageFile.write(img)
        imageFile.close()
        if wrote != fileSize:
            os.remove(imageFile.name)
            return None
        return imageFile.name


    def deleteGroupMsg(self, group, msgRandom, msgReq):
        con = hclt.HTTPConnection(self.url, timeout=5)
        con.request('POST', '/deletegroupmsg',
                    "fromqq={}&group={}&random={}&req={}".format(
                        self.qqid,
                        group,
                        msgRandom,
                        msgReq
                    ))
        res = con.getresponse().read()
        res = json.loads(res)
        return res


    def sendGroupMsg(self, text, group, anonymous=False):
        text = parse.quote(text)
        if anonymous:
            anonymous = "true"
        else:
            anonymous = "false"
        con = hclt.HTTPConnection(self.url, timeout=5)
        con.request('POST', '/sendgroupmsg',
                    "fromqq={}&togroup={}&text={}&anonymous={}".format(
                        self.qqid,
                        group,
                        text,
                        anonymous
                    ))
        res = con.getresponse().read()
        res = json.loads(res)
        return res


    def sendPrivateMsg(self, text, toqq):
        text = parse.quote(text)
        con = hclt.HTTPConnection(self.url, timeout=5)
        con.request('POST', '/sendprivatemsg',
                    "fromqq={}&toqq={}&text={}".format(
                        self.qqid,
                        toqq,
                        text
                    ))
        res = con.getresponse().read()
        res = json.loads(res)
        return res


    def sendJsonGroupMsg(self, group, jsonMsg, anonymous=False):
        try:
            text = json.dumps(jsonMsg)
        except Exception as err:
            print("failed to generate json string")
        text = parse.quote(text)
        if anonymous:
            anonymous = "true"
        else:
            anonymous = "false"
        con = hclt.HTTPConnection(self.url, timeout=5)
        con.request('POST', '/sendgroupjsonmsg',
                    "fromqq={}&togroup={}&json={}&anonymous={}".format(
                        self.qqid,
                        group,
                        text,
                        anonymous
                    ))
        res = con.getresponse().read()
        res = json.loads(res)
        return res


    def addGroup(self, group, text="Cody Bot"):
        con = hclt.HTTPConnection(self.url, timeout=5)
        con.request('POST', '/addgroup',
                    "fromqq={}&togroup={}&text={}".format(
                        self.qqid,
                        group,
                        text
                    ))
        res = con.getresponse().read()
        res = json.loads(res)
        return res


    def getGrouplist(self):
        con = hclt.HTTPConnection(self.url, timeout=5)
        con.request('POST', '/getgrouplist',
                    "logonqq={}".format(
                        self.qqid
                    ))
        res = con.getresponse().read()
        res = json.loads(res)
        return res


    def closeAPI(self):
        self.heartbeatClass.stopHeartbeat()
        self.removeSession()


def init():
    print("initializing Cody API...")

    global Cody
    Cody = CodyAPI(configFile="configs/Cody_QQ.json",
                   heartbeatClass=heartbeatControl())
    print("QQbot HTTP API url: {}".format(Cody.url))
    print("QQbot QQID: {}".format(Cody.qqid))
    print("groups that Cody managing:")
    for i in Cody.managingGroups:
        print(" ",i)
    try:
        sessionID = Cody.allocateSession()
        print("allocated QQbot session ID: {}".format(str(sessionID)))
    except Exception as err:
        print("failed to allocate session, {}".format(err))

    Cody.heartbeatClass.startHeartbeat()

    print("heartbeat thread started")

    print("Cody API initialized")


if __name__ == "__main__":
    init()
else:
    init()
