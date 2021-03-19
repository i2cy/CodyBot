#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author: i2cy(i2cy@outlook.com)
# Filename: main
# Created on: 2021/3/9

import i2cylib.database.sqlite as sqlib
import i2cylib.utils.path as putils
from i2cylib.utils.logger import *
from api.qqbot_api import *
from api.lewdity_api import *
import json
import os
import sys


CONFIG_PATH = "configs/codybot.json"

DEFAULT_CONFIG = {
    "qqapi": {
        "httpapi_address":  "127.0.0.1:10429",
        "bot_id":           1,
        "nickname":         "Cody",
        "qq_id":            88888888,
        "watchdog": {
            "host":             "127.0.0.1",
            "port":             10430,
            "dynkey":           "__BasiCABCKey.",
            "QQframe_timeout":  20
        }
    },
    "bot_configs": {
        "managing_groups":  [8888888],
        "OP_groups":        [8888888],
        "OP_users":         [8888888],
        "database":         "data/users.db",
        "log":              "log/codybot.log"
    },
    "lewdityapi": {
        "nsfw_painting_model":  "models/NSFW_painting_model.h5",
        "nsfw_photo_model":     "models/NSFW_photo_model.h5",
        "classification_model": "models/pic_classification_model.h5"
    }
}

global LOG, DB, CONF, BOT
TypeClassificationCNN = None
PaintingClassificationCNN = None
PhotoClassificationCNN = None

def write_conf(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)
        f.close()


def main():
    # 初始化
    global LOG, DB, CONF, BOT
    head = "[main]"
    LOG = logger()

    if not os.path.exists(CONFIG_PATH):
        LOG.WARNING("{} no config file was created, generating default config".format(head))
        putils.path_fixer(CONFIG_PATH)
        write_conf(CONFIG_PATH, DEFAULT_CONFIG)
        LOG.CRITICAL("{} edit the config first".format(head))
        return 1
    else:
        CONF = json.loads(open(CONFIG_PATH, "r").read())

    # path safety check
    paths = [CONFIG_PATH,
             CONF["bot_configs"]["database"],
             CONF["bot_configs"]["log"],
             CONF["lewdityapi"]["nsfw_painting_model"],
             CONF["lewdityapi"]["nsfw_photo_model"],
             CONF["lewdityapi"]["classification_model"]]

    for ele in paths:
        ret = putils.path_fixer(ele)
        if ret:
            LOG.WARNING("{} path to \"{}\" does not exist, fixed".format(head,
                                                                         ele))

    LOG = logger(CONF["bot_configs"]["log"])

    LOG.INFO("{} initializing...".format(head))

    # lewdity API
    global TypeClassificationCNN
    global PaintingClassificationCNN
    global PhotoClassificationCNN

    failure = False

    TypeClassificationCNN = customNN("Pic_Type_Classification")
    try:
        TypeClassificationCNN.load_model(CONF["lewdityapi"]["classification_model"])
        LOG.DEBUG("{} loaded model \"{}\"".format(head,
                                                  CONF["lewdityapi"]["classification_model"]))
    except Exception as err:
        failure = True
        LOG.ERROR("{} failed to load model \"{}\", {}".format(head,
                                                              CONF["lewdityapi"]["classification_model"],
                                                              err))

    PaintingClassificationCNN = customNN("Painting_Classification")
    try:
        PaintingClassificationCNN.load_model(CONF["lewdityapi"]["nsfw_painting_model"])
        LOG.DEBUG("{} loaded model \"{}\"".format(head,
                                                  CONF["lewdityapi"]["nsfw_painting_model"]))
    except Exception as err:
        failure = True
        LOG.ERROR("{} failed to load model \"{}\", {}".format(head,
                                                              CONF["lewdityapi"]["nsfw_painting_model"],
                                                              err))

    PhotoClassificationCNN = customNN("Photo_Classification")
    try:
        PhotoClassificationCNN.load_model(CONF["lewdityapi"]["nsfw_photo_model"])
        LOG.DEBUG("{} loaded model \"{}\"".format(head,
                                                  CONF["lewdityapi"]["nsfw_photo_model"]))
    except Exception as err:
        failure = True
        LOG.ERROR("{} failed to load model \"{}\", {}".format(head,
                                                              CONF["lewdityapi"]["nsfw_photo_model"],
                                                              err))
    if failure:
        LOG.WARNING("{} failed to initialize lewdity API".format(head))
    else:
        LOG.INFO("{} lewdity API initialized".format(head))

    # qqbot api
    global BOT

    failure = False

    try:
        configs = {
            "URL":  CONF["qqapi"]["httpapi_address"],
            "ID":   CONF["qqapi"]["bot_id"],
            "QQID": CONF["qqapi"]["qq_id"],
            "Nick": CONF["qqapi"]["nickname"],
            "HeartbeatHost":    CONF["qqapi"]["watchdog"]["host"],
            "HeartbeatPort":    CONF["qqapi"]["watchdog"]["port"],
            "TimeKey":          CONF["qqapi"]["watchdog"]["dynkey"],
            "QQframeRestartThreshold":  CONF["qqapi"]["watchdog"]["QQframe_timeout"]
        }
    except Exception as err:
        LOG.WARNING("{} failed to load qqbot configs, please check your configs,"
                    " {}".format(head, err))
        failure = True

    try:
        BOT = CodyAPI(config=configs, heartbeatClass=heartbeatControl(log=LOG))
        LOG.DEBUG("{} qqbot HTTPAPI url: {}".format(head, BOT.url))
        LOG.DEBUG("{} qqbot QQID: {}".format(head, BOT.qqid))
        LOG.DEBUG("{} codyapi initialized".format(head))
    except Exception as err:
        LOG.WARNING("{} failed to initialize CodyAPI, {}".format(head, err))
        failure = True

    try:
        session_id = BOT.allocateSession()
        LOG.DEBUG("{} allocated qqbot session ID: {}".format(head, session_id))
    except Exception as err:
        LOG.WARNING("{} failed to allocate session, {}".format(head, err))

    try:
        BOT.heartbeatClass.startHeartbeat()
        LOG.DEBUG("{} watchdog heartbeat started".format(head))
    except Exception as err:
        LOG.WARNING("{} failed to start watchdog, {}".format(head, err))
        failure = True

    if failure:
        LOG.CRITICAL("{} failed to initialize qqbot api".format(head))
        return 1
    else:
        LOG.INFO("{} qqbot API initialized".format(head))


if __name__ == '__main__':
    ret = main()
    sys.exit(ret)
