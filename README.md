## Python Interpreter
`Python3.7`

## Third-party Library Requirements：
`Tensorflow2.3`
`matplotlib`
`opencv-python`
`psutil`

## QQ bot Framework:
`小栗子框架` [论坛链接]
the qq bot framework included in this repo is version 2.7.1

[论坛链接]: https://bbs.xiaolz.cn/forum.php

## Remote Windows(VM) entry:
`vm_side/main.py`
 - Usage:
    1. prepare a Windows environment with internal-only network connected
    2. install Python3 environment
    3. copy `vm_side` folder to Windows environment
    4. run main.py (do not move any files in that folder)
 - Notification:
    Notice that the first running you will need to login your target QQ in XiaoLiZi QQ frame,
    which you could follow the instructions that on the program window (_XiaoLiZi_).
    

## Bot entry:
`main.py` or `main_beta.py`
 - Usage:
    1. make sure you have done the **Remote Windows(VM) entry** within instructions
    2. run **`main.py`** (_or `main_beta.py`_) at background
include_all_commits=true

## Project Xmind Document
I uploaded the xmind document of this project to this repo too.
Check it in `document` folder

## Default config example:
```{
  "URL": "192.168.31.29:10429",
  "HeartbeatHost": "192.168.31.29",
  "HeartbeatPort": 10430,
  "TimeKey": "__BasiCABCKey.",
  "QQframeRestartThreshold": 20,
  "ID": 1,
  "QQID": "00000000",
  "Nick": "Cody",
  "ManagingGroups": [
    000000002,
    000000001
  ],
  "OPGroups": [
    000000001
  ]
}
