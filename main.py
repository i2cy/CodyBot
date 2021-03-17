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


CONFIG_PATH = "configs/codybot.json"


DEFAULT_CONFIG = {
    "codyapi": {
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
    }
}


def write_conf(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)
        f.close()


def main():
    # 初始化
    global LOG, DB, CONF
    head = "[main]"
    LOG = logger()
    if not os.path.exists(CONFIG_PATH):
        LOG.WARNING("{} no config file was created, generating default config")
        putils.path_fixer(CONFIG_PATH)
        write_conf(CONFIG_PATH, DEFAULT_CONFIG)
        CONF = DEFAULT_CONFIG
    else:
        CONF = json.loads(open(CONFIG_PATH, "r").read())

    LOG.INFO("{} initializing".format(head))


if __name__ == '__main__':
    main()
