#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author: i2cy(i2cy@outlook.com)
# Filename: get_pony.py
# Created on: 2020/8/30

from derpibooru import Search, query, sort
from urllib import request
import time


DATASET_ROOT = "datasets/ponies"
LIMITS = 10000
KEY = "nB8iNyxV4ZRaUeqRV4Eh"

bad_pony = {
    "safe",
    "-comic",
    "-text only",
    "-animated",
    query.height <= 2400
}



print("fetching good ponies...")

msg = ""
offset = 0
offset_temp = 0
while offset_temp < LIMITS:
    try:
        for index, img in enumerate(Search().key(KEY).query(*bad_pony).limit(LIMITS-offset).sort_by(sort.RANDOM)):
            offset_temp = index + offset
            msg_len = len(msg)
            msg = "fetched {} images, now fetching: {}".format(str(index), img.image)
            print("\r" + " "*msg_len + "\r" + msg, end="")
            try:
                f = open("{}/safe/{}.{}".format(DATASET_ROOT,
                                                str(index+offset), img.format), "wb")
                f.write((request.urlopen(img.medium, timeout=15)).read())
                f.close()
            except:
                continue
    except Exception as err:
        offset = offset_temp
        print("\ncaught an exception:", err)
    time.sleep(10)
print("")


print("all done!")
