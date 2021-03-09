#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author: i2cy(i2cy@outlook.com)
# Filename: test_main
# Created on: 2020/9/14

from api.lewdity_api import *
from api.qqbot_api import *
import threading
import time
import os

LOOP_TIME = 1
CACHE_DIR = "codyCache/"
REFRESHING_TIME = 3600*24
MUTE_THRESHOLD = 2
MUTE_TIME = 3600*2*0

EVENTS = []
LIVE = True
MUTE_LIST = {}
TOTAL_CLASSIFICATED = 0

"""
{"<QQID>":{
  "lewd_time": <lewd_count>
}}
"""


def path_fixer(path):  # path checker
    chk = ""
    for i in path:
        chk += i
        if i in ("/", "\\"):
            if not os.path.exists(chk):
                os.mkdir(chk)


def event_loop():
    global EVENTS, Cody
    while LIVE:
        try:
            EVENTS += Cody.getEvent()
        except:
            continue
        time.sleep(LOOP_TIME)
    for i in Cody.managingGroups:
        Cody.sendGroupMsg("event listening loop thread stopped", i)


def check_and_mute(event):
    global Cody, TOTAL_CLASSIFICATED, MUTE_LIST
    if event["Type"] != "GroupMsg":
        return "ignored"
    groupID = str(event["FromGroup"]["GIN"])
    if not groupID in Cody.managingGroups:
        return "ignored group {}".format(groupID)
    msg = event["Msg"]["Text"]

    pic_urls = Cody.getPicUrl(msg, groupID)

    if pic_urls == []:
        return "not picture msg"

    info = ""

    for pic_url in pic_urls:
        print(pic_url)
        pic_hash = pic_url["hash"]
        pic_url = pic_url["url"]

        pic_filename = "{}{}".format(CACHE_DIR, pic_hash)
        if os.path.exists(pic_filename+".jpeg"):
            pic_filename = pic_filename+".jpeg"
            res = {"lewd": True}
        elif os.path.exists(pic_filename+".png"):
            pic_filename = pic_filename+".png"
            res = {"lewd": True}
        elif os.path.exists(pic_filename+".gif"):
            pic_filename = pic_filename+".gif"
            res = {"lewd": True}
        else:
            try:
                pic_filename = Cody.downloadPic(pic_url, pic_filename)
            except:
                try:
                    pic_filename = Cody.downloadPic(pic_url, pic_filename)
                except Exception as err:
                    info = "failed twice to get picture file, {}".format(str(err))
                    continue
            if pic_filename == None:
                info = "failed to get picture file"
                continue
            TOTAL_CLASSIFICATED += 1
            print("classificating picture \"{}\", total amount {}".format(
                pic_filename, TOTAL_CLASSIFICATED
            ))
            res = classificateAPI(pic_filename)
            print("classification result: \n{}".format(res))

        if not res["lewd"]:
            os.remove(pic_filename)
            info = "not lewd"
            continue

        targetQQID = str(event["FromQQ"]["UIN"])
        msgReq = event["Msg"]["Req"]
        msgRandom = event["Msg"]["Random"]

        Cody.sendGroupMsg("Cody beta have detected something lewd", groupID)
        Cody.sendGroupMsg("internal data:\n{}".format(str(res)), groupID)
        Cody.deleteGroupMsg(groupID, msgRandom, msgReq)

        if targetQQID in MUTE_LIST.keys():
            MUTE_LIST[targetQQID]["lewd_time"] += 1
        else:
            MUTE_LIST.update({targetQQID:{
                "lewd_time": 1
            }})

        if MUTE_LIST[targetQQID]["lewd_time"] >= MUTE_THRESHOLD:
            print("muting {} for {} seconds in group {}".format(
                targetQQID,
                MUTE_TIME,
                groupID
            ))
            ret = Cody.mute(targetQQID, MUTE_TIME, groupID)
            print("muting status: {}".format(str(ret)))

        return "lewd detected"

    return info


def check_loop():
    global EVENTS, MUTE_LIST, Cody
    time_stamp = time.time()
    while LIVE:
        try:
            if time.time() - time_stamp > REFRESHING_TIME:
                for i in MUTE_LIST:
                    MUTE_LIST[i]["lewd_time"] = MUTE_LIST[i]["lewd_time"] - 1
            events = EVENTS
            EVENTS = []
            if events == []:
                time.sleep(LOOP_TIME/4)
                continue
            for i in events:
                try:
                    ret = check_and_mute(i)
                    print("event checking status with text \"{}\": {}".format(
                        i["Msg"]["Text"], ret
                    ))
                except Exception as err:
                    try:
                        print("failed to check event with text \"{}\", {}, retring".format(
                            i["Msg"]["Text"], err
                        ))
                        ret = check_and_mute(i)
                    except Exception as err:
                        print("failed again to check event with text \"{}\", {}".format(
                            i["Msg"]["Text"], err))
        except Exception as err:
            print("error in checking loop,", err)
    for i in Cody.managingGroups:
        try:
            Cody.sendGroupMsg("checking loop thread stopped", i)
        except Exception as err:
            print("failed to send start message,", err)


def main():
    global LIVE
    print("checking cache path")
    path_fixer(CACHE_DIR)
    eventLoop = threading.Thread(target=event_loop)
    eventLoop.start()
    print("events listening loop started")
    checkloop = threading.Thread(target=check_loop)
    checkloop.start()
    print("qqbot api watchdog started")
    time.sleep(2)
    for i in Cody.managingGroups:
        try:
            Cody.sendGroupMsg("all threads started", i)
        except Exception as err:
            print("failed to send boot message, ", err)
    while True:
        try:
            ctrl = input('(use Ctrl+C to exit)\n')
        except KeyboardInterrupt:
            LIVE = False
            time.sleep(LOOP_TIME)
            Cody.closeAPI()
            exit(0)


if __name__ == "__main__":
    main()
