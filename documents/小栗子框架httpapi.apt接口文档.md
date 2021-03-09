
## 申请会话(缓冲区)

#### 接口URL
> {{url}}/allocsession

#### 请求方式
> POST

#### Content-Type
> urlencoded







#### 成功响应示例
```javascript
{
	"session_id": 1
}
```



## 删除会话(缓冲区)

#### 接口URL
> {{url}}/removesession

#### 请求方式
> POST

#### Content-Type
> urlencoded






#### 请求Body参数

| 参数        | 示例值   | 是否必填   |  参数描述  |
| :--------   | :-----  | :-----  | :----  |
| sessid     | 1 |  必填 | 指定会话(缓冲区)id |

#### 成功响应示例
```javascript
{
	"status": "OK"
}
```



## 清空事件缓冲区

#### 接口URL
> {{url}}/resetevent

#### 请求方式
> POST

#### Content-Type
> urlencoded






#### 请求Body参数

| 参数        | 示例值   | 是否必填   |  参数描述  |
| :--------   | :-----  | :-----  | :----  |
| sessid     | 1 |  必填 | 指定会话(缓冲区)id |

#### 成功响应示例
```javascript
{
	"status": "OK"
}
```



## 获取并清空事件缓冲区

#### 接口URL
> {{url}}/getevent

#### 请求方式
> POST

#### Content-Type
> urlencoded






#### 请求Body参数

| 参数        | 示例值   | 是否必填   |  参数描述  |
| :--------   | :-----  | :-----  | :----  |
| sessid     | 1 |  必填 | 指定会话(缓冲区)id |



## 获取并清空事件缓冲区v2(支持直接解析json)

#### 接口URL
> {{url}}/geteventv2

#### 请求方式
> POST

#### Content-Type
> urlencoded






#### 请求Body参数

| 参数        | 示例值   | 是否必填   |  参数描述  |
| :--------   | :-----  | :-----  | :----  |
| sessid     | 1 |  必填 | 指定会话(缓冲区)id |



## 登录指定QQ

#### 接口URL
> {{url}}/loginqq

#### 请求方式
> POST

#### Content-Type
> urlencoded






#### 请求Body参数

| 参数        | 示例值   | 是否必填   |  参数描述  |
| :--------   | :-----  | :-----  | :----  |
| logonqq     | 123456789 |  必填 | 指定框架QQ |



## 下线指定QQ

#### 接口URL
> {{url}}/logoutqq

#### 请求方式
> POST

#### Content-Type
> urlencoded






#### 请求Body参数

| 参数        | 示例值   | 是否必填   |  参数描述  |
| :--------   | :-----  | :-----  | :----  |
| logonqq     | 123456789 |  必填 | 指定框架QQ |



## 发送好友消息

#### 接口URL
> {{url}}/sendprivatemsg

#### 请求方式
> POST

#### Content-Type
> urlencoded






#### 请求Body参数

| 参数        | 示例值   | 是否必填   |  参数描述  |
| :--------   | :-----  | :-----  | :----  |
| fromqq     | 123456789 |  必填 | 指定框架QQ |
| toqq     | 987654321 |  必填 | 指定好友QQ |
| text     | - |  必填 | 指定消息内容(存在特殊字符请使用URL编码) |



## 发送群消息

#### 接口URL
> {{url}}/sendgroupmsg

#### 请求方式
> POST

#### Content-Type
> urlencoded






#### 请求Body参数

| 参数        | 示例值   | 是否必填   |  参数描述  |
| :--------   | :-----  | :-----  | :----  |
| fromqq     | 123456789 |  必填 | 指定框架QQ |
| togroup     | 12345678 |  必填 | 指定群号 |
| text     | - |  必填 | 指定消息内容(存在特殊字符请使用URL编码) |
| anonymous     | - |  选填 | 指定是否匿名(true,false) |



## 发送群临时消息

#### 接口URL
> {{url}}/sendgrouptempmsg

#### 请求方式
> POST

#### Content-Type
> urlencoded






#### 请求Body参数

| 参数        | 示例值   | 是否必填   |  参数描述  |
| :--------   | :-----  | :-----  | :----  |
| fromqq     | - |  必填 | 指定框架QQ |
| togroup     | - |  必填 | 指定群号 |
| toqq     | - |  必填 | 指定对方QQ |
| text     | - |  必填 | 指定消息内容(特殊字符请使用URL编码) |



## 发送输入状态

#### 接口URL
> {{url}}/sendinputstatus

#### 请求方式
> POST

#### Content-Type
> urlencoded






#### 请求Body参数

| 参数        | 示例值   | 是否必填   |  参数描述  |
| :--------   | :-----  | :-----  | :----  |
| logonqq     | 123456789 |  必填 | 指定框架QQ |
| toqq     | - |  选填 | 指定对方QQ |
| status     | - |  选填 | 输入状态。1:正在输入,2:关闭显示,3:正在说话。默认为1 |



## 打好友电话
可向好友发起语音通话(不能传递语音数据)，不建议频繁使用
#### 接口URL
> {{url}}/callfriend

#### 请求方式
> POST

#### Content-Type
> urlencoded






#### 请求Body参数

| 参数        | 示例值   | 是否必填   |  参数描述  |
| :--------   | :-----  | :-----  | :----  |
| logonqq     | 123456789 |  必填 | 指定框架QQ |
| toqq     | - |  选填 | 指定对方QQ |



## 添加好友

#### 接口URL
> {{url}}/addfriend

#### 请求方式
> POST

#### Content-Type
> urlencoded






#### 请求Body参数

| 参数        | 示例值   | 是否必填   |  参数描述  |
| :--------   | :-----  | :-----  | :----  |
| fromqq     | - |  必填 | 指定框架QQ |
| toqq     | - |  必填 | 指定对方QQ |
| text     | - |  选填 | 指定附言 |
| remark     | - |  选填 | 指定备注 |



## 添加群

#### 接口URL
> {{url}}/addgroup

#### 请求方式
> POST

#### Content-Type
> urlencoded






#### 请求Body参数

| 参数        | 示例值   | 是否必填   |  参数描述  |
| :--------   | :-----  | :-----  | :----  |
| fromqq     | - |  必填 | 指定框架QQ |
| togroup     | - |  必填 | 指定群号 |
| text     | - |  选填 | 指定附言 |



## 删除好友

#### 接口URL
> {{url}}/deletefriend

#### 请求方式
> POST

#### Content-Type
> urlencoded






#### 请求Body参数

| 参数        | 示例值   | 是否必填   |  参数描述  |
| :--------   | :-----  | :-----  | :----  |
| fromqq     | - |  必填 | 指定框架QQ |
| toqq     | - |  必填 | 指定对方QQ |



## 置屏蔽好友

#### 接口URL
> {{url}}/setfriendignmsg

#### 请求方式
> POST

#### Content-Type
> urlencoded






#### 请求Body参数

| 参数        | 示例值   | 是否必填   |  参数描述  |
| :--------   | :-----  | :-----  | :----  |
| fromqq     | - |  必填 | 指定框架QQ |
| toqq     | - |  必填 | 指定对方QQ |
| ignore     | - |  必填 | 指定是否屏蔽(true,false) |



## 置特别关心好友

#### 接口URL
> {{url}}/setfriendcare

#### 请求方式
> POST

#### Content-Type
> urlencoded






#### 请求Body参数

| 参数        | 示例值   | 是否必填   |  参数描述  |
| :--------   | :-----  | :-----  | :----  |
| fromqq     | - |  必填 | 指定框架QQ |
| toqq     | - |  必填 | 指定对方QQ |
| care     | - |  必填 | 指定是否关心(true,false) |



## 发送好友JSON消息

#### 接口URL
> {{url}}/sendprivatejsonmsg

#### 请求方式
> POST

#### Content-Type
> urlencoded






#### 请求Body参数

| 参数        | 示例值   | 是否必填   |  参数描述  |
| :--------   | :-----  | :-----  | :----  |
| fromqq     | - |  必填 | 指定框架QQ |
| toqq     | - |  必填 | 指定对方QQ |
| json     | - |  必填 | 指定消息内容(存在特殊字符请使用URL编码) |



## 发送群JSON消息

#### 接口URL
> {{url}}/sendgroupjsonmsg

#### 请求方式
> POST

#### Content-Type
> urlencoded






#### 请求Body参数

| 参数        | 示例值   | 是否必填   |  参数描述  |
| :--------   | :-----  | :-----  | :----  |
| fromqq     | - |  必填 | 指定框架QQ |
| togroup     | - |  必填 | 指定群号 |
| json     | - |  必填 | 指定消息内容(存在特殊字符请使用URL编码) |
| anonymous     | - |  选填 | 指定是否匿名(true,false) |



## 上传好友图片
返回值可用于发送图片
#### 接口URL
> {{url}}/sendprivatepic

#### 请求方式
> POST

#### Content-Type
> urlencoded






#### 请求Body参数

| 参数        | 示例值   | 是否必填   |  参数描述  |
| :--------   | :-----  | :-----  | :----  |
| fromqq     | - |  必填 | 指定框架QQ |
| toqq     | - |  必填 | 指定好友QQ |
| fromtype     | - |  选填 | 指定图片来源类型(0:pic参数,1:本地文件,2:网络文件 默认为0) |
| pic     | - |  必填 | [fromtype=0时]指定数据(请使用BASE64+URL编码:url_encode(base64_encode(src))) |
| path     | - |  必填 | [fromtype=1时]指定文件路径(请使用绝对路径,存在特殊字符请使用URL编码) |
| url     | - |  必填 | [fromtype=2时]指定文件url(存在特殊字符请使用URL编码) |
| flashpic     | - |  选填 | 指定是否闪照(true,false) |



## 上传群图片
返回值可用于发送图片
#### 接口URL
> {{url}}/sendgrouppic

#### 请求方式
> POST

#### Content-Type
> urlencoded






#### 请求Body参数

| 参数        | 示例值   | 是否必填   |  参数描述  |
| :--------   | :-----  | :-----  | :----  |
| fromqq     | - |  必填 | 指定框架QQ |
| togroup     | - |  必填 | 指定群号 |
| fromtype     | - |  选填 | 指定图片来源类型(0:pic参数,1:本地文件,2:网络文件 默认为0) |
| pic     | - |  必填 | [fromtype=0时]指定数据(请使用BASE64+URL编码:url_encode(base64_encode(src))) |
| path     | - |  必填 | [fromtype=1时]指定文件路径(请使用绝对路径,存在特殊字符请使用URL编码) |
| url     | - |  必填 | [fromtype=2时]指定文件url(存在特殊字符请使用URL编码) |
| flashpic     | - |  选填 | 指定是否闪照(true,false) |



## 向好友发送语音

#### 接口URL
> {{url}}/sendprivateaudio

#### 请求方式
> POST

#### Content-Type
> urlencoded






#### 请求Body参数

| 参数        | 示例值   | 是否必填   |  参数描述  |
| :--------   | :-----  | :-----  | :----  |
| fromqq     | - |  必填 | 指定框架QQ |
| toqq     | - |  必填 | 指定好友QQ |
| type     | - |  选填 | 指定语音类型(0普通语音,1变声语音,2文字语音,3红包匹配语音) |
| text     | - |  选填 | 指定语音文字 |
| fromtype     | - |  选填 | 指定语音来源类型(0:pic参数,1:本地文件,2:网络文件 默认为0) |
| audio     | - |  必填 | [fromtype=0时]指定数据(请使用BASE64+URL编码:url_encode(base64_encode(src))) |
| path     | - |  必填 | [fromtype=1时]指定文件路径(请使用绝对路径,存在特殊字符请使用URL编码) |
| url     | - |  必填 | [fromtype=2时]指定文件url(存在特殊字符请使用URL编码) |



## 向群发送语音

#### 接口URL
> {{url}}/sendgroupaudio

#### 请求方式
> POST

#### Content-Type
> urlencoded






#### 请求Body参数

| 参数        | 示例值   | 是否必填   |  参数描述  |
| :--------   | :-----  | :-----  | :----  |
| fromqq     | - |  必填 | 指定框架QQ |
| togroup     | - |  必填 | 指定群号 |
| type     | - |  选填 | 指定语音类型(0普通语音,1变声语音,2文字语音,3红包匹配语音) |
| text     | - |  选填 | 指定语音文字 |
| fromtype     | - |  选填 | 指定语音来源类型(0:pic参数,1:本地文件,2:网络文件 默认为0) |
| audio     | - |  必填 | [fromtype=0时]指定数据(请使用BASE64+URL编码:url_encode(base64_encode(src))) |
| path     | - |  必填 | [fromtype=1时]指定文件路径(请使用绝对路径,存在特殊字符请使用URL编码) |
| url     | - |  必填 | [fromtype=2时]指定文件url(存在特殊字符请使用URL编码) |



## 上传头像

#### 接口URL
> {{url}}/uploadfacepic

#### 请求方式
> POST

#### Content-Type
> urlencoded






#### 请求Body参数

| 参数        | 示例值   | 是否必填   |  参数描述  |
| :--------   | :-----  | :-----  | :----  |
| fromqq     | - |  必填 | 指定框架QQ |
| fromtype     | - |  选填 | 指定图片来源类型(0:pic参数,1:本地文件,2:网络文件 默认为0) |
| pic     | - |  必填 | [fromtype=0时]指定数据(请使用BASE64+URL编码:url_encode(base64_encode(src))) |
| path     | - |  必填 | [fromtype=1时]指定文件路径(请使用绝对路径,存在特殊字符请使用URL编码) |
| url     | - |  必填 | [fromtype=2时]指定文件url(存在特殊字符请使用URL编码) |



## 上传群头像

#### 接口URL
> {{url}}/uploadgroupfacepic

#### 请求方式
> POST

#### Content-Type
> urlencoded






#### 请求Body参数

| 参数        | 示例值   | 是否必填   |  参数描述  |
| :--------   | :-----  | :-----  | :----  |
| fromqq     | - |  必填 | 指定框架QQ |
| group     | - |  必填 | 指定群号 |
| fromtype     | - |  选填 | 指定图片来源类型(0:pic参数,1:本地文件,2:网络文件 默认为0) |
| pic     | - |  必填 | [fromtype=0时]指定数据(请使用BASE64+URL编码:url_encode(base64_encode(src))) |
| path     | - |  必填 | [fromtype=1时]指定文件路径(请使用绝对路径,存在特殊字符请使用URL编码) |
| url     | - |  必填 | [fromtype=2时]指定文件url(存在特殊字符请使用URL编码) |



## 设置群名片

#### 接口URL
> {{url}}/setgroupcard

#### 请求方式
> POST

#### Content-Type
> urlencoded






#### 请求Body参数

| 参数        | 示例值   | 是否必填   |  参数描述  |
| :--------   | :-----  | :-----  | :----  |
| fromqq     | - |  必填 | 指定框架QQ |
| togroup     | - |  必填 | 指定群号 |
| toqq     | - |  必填 | 指定群成员QQ |
| card     | - |  必填 | 指定群名片(存在特殊字符请使用URL编码) |



## 取昵称

#### 接口URL
> {{url}}/getnickname

#### 请求方式
> POST

#### Content-Type
> urlencoded






#### 请求Body参数

| 参数        | 示例值   | 是否必填   |  参数描述  |
| :--------   | :-----  | :-----  | :----  |
| fromqq     | - |  必填 | [不使用缓存则必须,使用缓存则不须]指定框架QQ |
| toqq     | - |  必填 | 指定对方QQ |
| fromcache     | - |  必填 | 指定是否使用缓存(true,false) |



## 从缓存取群名称

#### 接口URL
> {{url}}/getgroupnamefromcache

#### 请求方式
> POST

#### Content-Type
> urlencoded






#### 请求Body参数

| 参数        | 示例值   | 是否必填   |  参数描述  |
| :--------   | :-----  | :-----  | :----  |
| group     | - |  必填 | 指定群号 |



## 取框架QQ

#### 接口URL
> {{url}}/getlogonqq

#### 请求方式
> POST

#### Content-Type
> urlencoded









## 取好友列表

#### 接口URL
> {{url}}/getfriendlist

#### 请求方式
> POST

#### Content-Type
> urlencoded






#### 请求Body参数

| 参数        | 示例值   | 是否必填   |  参数描述  |
| :--------   | :-----  | :-----  | :----  |
| logonqq     | - |  必填 | 指定框架QQ |



## 取群列表

#### 接口URL
> {{url}}/getgrouplist

#### 请求方式
> POST

#### Content-Type
> urlencoded






#### 请求Body参数

| 参数        | 示例值   | 是否必填   |  参数描述  |
| :--------   | :-----  | :-----  | :----  |
| logonqq     | - |  必填 | 指定框架QQ |



## 取群成员列表

#### 接口URL
> {{url}}/getgroupmemberlist

#### 请求方式
> POST

#### Content-Type
> urlencoded






#### 请求Body参数

| 参数        | 示例值   | 是否必填   |  参数描述  |
| :--------   | :-----  | :-----  | :----  |
| logonqq     | - |  必填 | 指定框架QQ |
| group     | - |  必填 | 指定群号 |



## 设置管理员

#### 接口URL
> {{url}}/setgroupmgr

#### 请求方式
> POST

#### Content-Type
> urlencoded






#### 请求Body参数

| 参数        | 示例值   | 是否必填   |  参数描述  |
| :--------   | :-----  | :-----  | :----  |
| fromqq     | - |  必填 | 指定框架QQ |
| group     | - |  必填 | 指定群号 |
| toqq     | - |  必填 | 指定对方QQ |
| bemgr     | - |  必填 | 是否成为管理员(true,false) |



## 取管理层列表

#### 接口URL
> {{url}}/getgroupmgrlist

#### 请求方式
> POST

#### Content-Type
> urlencoded






#### 请求Body参数

| 参数        | 示例值   | 是否必填   |  参数描述  |
| :--------   | :-----  | :-----  | :----  |
| fromqq     | - |  必填 | 指定框架QQ |
| group     | - |  必填 | 指定群号 |



## 取群名片

#### 接口URL
> {{url}}/getgroupcard

#### 请求方式
> POST

#### Content-Type
> urlencoded






#### 请求Body参数

| 参数        | 示例值   | 是否必填   |  参数描述  |
| :--------   | :-----  | :-----  | :----  |
| fromqq     | - |  必填 | 指定框架QQ |
| group     | - |  必填 | 指定群号 |
| toqq     | - |  必填 | 指定对方QQ |



## 取个性签名

#### 接口URL
> {{url}}/getsignat

#### 请求方式
> POST

#### Content-Type
> urlencoded






#### 请求Body参数

| 参数        | 示例值   | 是否必填   |  参数描述  |
| :--------   | :-----  | :-----  | :----  |
| fromqq     | - |  必填 | 指定框架QQ |
| toqq     | - |  必填 | 指定对方QQ |



## 设置昵称

#### 接口URL
> {{url}}/setnickname

#### 请求方式
> POST

#### Content-Type
> urlencoded






#### 请求Body参数

| 参数        | 示例值   | 是否必填   |  参数描述  |
| :--------   | :-----  | :-----  | :----  |
| fromqq     | - |  必填 | 指定框架QQ |
| nickname     | - |  必填 | 指定昵称 |



## 设置个性签名

#### 接口URL
> {{url}}/setsignat

#### 请求方式
> POST

#### Content-Type
> urlencoded






#### 请求Body参数

| 参数        | 示例值   | 是否必填   |  参数描述  |
| :--------   | :-----  | :-----  | :----  |
| fromqq     | - |  必填 | 指定框架QQ |
| signature     | - |  必填 | 指定个性签名 |



## 修改资料
生日、家乡、所在地 参数格式和子参数数量必须正确，否则修改资料无法成功，不需要修改的项就不要填
#### 接口URL
> {{url}}/updatedata

#### 请求方式
> POST

#### Content-Type
> urlencoded






#### 请求Body参数

| 参数        | 示例值   | 是否必填   |  参数描述  |
| :--------   | :-----  | :-----  | :----  |
| logonqq     | 123456789 |  必填 | 指定框架QQ |
| nick     | - |  选填 | 昵称 |
| sex     | - |  选填 | 性别。1:男 2:女,默认男。 |
| birth     | - |  选填 | 生日。格式：2020/5/5 均为整数。 |
| profession     | - |  选填 | 职业。1:IT,2:制造,3:医疗,4:金融,5:商业,6:文化,7:艺术,8:法律,9:教育,10:行政,11:模特,12:空姐,13:学生,14:其他职业，默认1。 |
| company     | - |  选填 | 公司名 |
| location     | - |  选填 | 所在地。国家代码|省份代码|市代码|区字母|区代码，如：49|13110|56|NK|51，表示中国江西省吉安市青原区，这些数据是腾讯的数据，非国际数据。 |
| home     | - |  选填 | 家乡。国家代码|省份代码|市代码|区字母|区代码，如：49|13110|56|NK|51，表示中国江西省吉安市青原区，这些数据是腾讯的数据，非国际数据。 |
| email     | - |  选填 | 邮箱 |
| desc     | - |  选填 | 个人说明 |



## 移出群成员

#### 接口URL
> {{url}}/kickgroupmember

#### 请求方式
> POST

#### Content-Type
> urlencoded






#### 请求Body参数

| 参数        | 示例值   | 是否必填   |  参数描述  |
| :--------   | :-----  | :-----  | :----  |
| fromqq     | - |  必填 | 指定框架QQ |
| group     | - |  必填 | 指定群号 |
| toqq     | - |  必填 | 指定对方QQ |
| ignoreaddgrequest     | - |  选填 | 拒绝再加群申请(true,false) |



## 禁言群成员

#### 接口URL
> {{url}}/mutegroupmember

#### 请求方式
> POST

#### Content-Type
> urlencoded






#### 请求Body参数

| 参数        | 示例值   | 是否必填   |  参数描述  |
| :--------   | :-----  | :-----  | :----  |
| fromqq     | - |  必填 | 指定框架QQ |
| group     | - |  必填 | 指定群号 |
| toqq     | - |  必填 | 指定对方QQ |
| time     | - |  必填 | 指定禁言时长(以秒计) |



## 退群

#### 接口URL
> {{url}}/exitgroup

#### 请求方式
> POST

#### Content-Type
> urlencoded






#### 请求Body参数

| 参数        | 示例值   | 是否必填   |  参数描述  |
| :--------   | :-----  | :-----  | :----  |
| fromqq     | - |  必填 | 指定框架QQ |
| group     | - |  必填 | 指定群号 |



## 解散群

#### 接口URL
> {{url}}/dispgroup

#### 请求方式
> POST

#### Content-Type
> urlencoded






#### 请求Body参数

| 参数        | 示例值   | 是否必填   |  参数描述  |
| :--------   | :-----  | :-----  | :----  |
| fromqq     | - |  必填 | 指定框架QQ |
| group     | - |  必填 | 指定群号 |



## 全员禁言

#### 接口URL
> {{url}}/setgroupwholemute

#### 请求方式
> POST

#### Content-Type
> urlencoded






#### 请求Body参数

| 参数        | 示例值   | 是否必填   |  参数描述  |
| :--------   | :-----  | :-----  | :----  |
| fromqq     | - |  必填 | 指定框架QQ |
| group     | - |  必填 | 指定群号 |
| ismute     | - |  必填 | 指定是否禁言(true,false) |



## 置群员权限_发起新的群聊

#### 接口URL
> {{url}}/setgrouppriv_newgroup

#### 请求方式
> POST

#### Content-Type
> urlencoded






#### 请求Body参数

| 参数        | 示例值   | 是否必填   |  参数描述  |
| :--------   | :-----  | :-----  | :----  |
| fromqq     | - |  必填 | 指定框架QQ |
| togroup     | - |  必填 | 指定群号 |
| allow     | - |  必填 | 指定是否允许(true,false) |



## 置群员权限_发起临时会话

#### 接口URL
> {{url}}/setgrouppriv_newtempsession

#### 请求方式
> POST

#### Content-Type
> urlencoded






#### 请求Body参数

| 参数        | 示例值   | 是否必填   |  参数描述  |
| :--------   | :-----  | :-----  | :----  |
| fromqq     | - |  必填 | 指定框架QQ |
| togroup     | - |  必填 | 指定群号 |
| allow     | - |  必填 | 指定是否允许(true,false) |



## 置群员权限_上传文件

#### 接口URL
> {{url}}/setgrouppriv_uploadfile

#### 请求方式
> POST

#### Content-Type
> urlencoded






#### 请求Body参数

| 参数        | 示例值   | 是否必填   |  参数描述  |
| :--------   | :-----  | :-----  | :----  |
| fromqq     | - |  必填 | 指定框架QQ |
| togroup     | - |  必填 | 指定群号 |
| allow     | - |  必填 | 指定是否允许(true,false) |



## 置群员权限_上传相册

#### 接口URL
> {{url}}/setgrouppriv_uploadphotoalbum

#### 请求方式
> POST

#### Content-Type
> urlencoded






#### 请求Body参数

| 参数        | 示例值   | 是否必填   |  参数描述  |
| :--------   | :-----  | :-----  | :----  |
| fromqq     | - |  必填 | 指定框架QQ |
| togroup     | - |  必填 | 指定群号 |
| allow     | - |  必填 | 指定是否允许(true,false) |



## 置群员权限_邀请他人加群

#### 接口URL
> {{url}}/setgrouppriv_invitein

#### 请求方式
> POST

#### Content-Type
> urlencoded






#### 请求Body参数

| 参数        | 示例值   | 是否必填   |  参数描述  |
| :--------   | :-----  | :-----  | :----  |
| fromqq     | - |  必填 | 指定框架QQ |
| togroup     | - |  必填 | 指定群号 |
| allow     | - |  必填 | 指定是否允许(true,false) |



## 置群员权限_匿名聊天

#### 接口URL
> {{url}}/setgrouppriv_anonymous

#### 请求方式
> POST

#### Content-Type
> urlencoded






#### 请求Body参数

| 参数        | 示例值   | 是否必填   |  参数描述  |
| :--------   | :-----  | :-----  | :----  |
| fromqq     | - |  必填 | 指定框架QQ |
| togroup     | - |  必填 | 指定群号 |
| allow     | - |  必填 | 指定是否允许(true,false) |



## 置群员权限_坦白说

#### 接口URL
> {{url}}/setgrouppriv_tanbaishuo

#### 请求方式
> POST

#### Content-Type
> urlencoded






#### 请求Body参数

| 参数        | 示例值   | 是否必填   |  参数描述  |
| :--------   | :-----  | :-----  | :----  |
| fromqq     | - |  必填 | 指定框架QQ |
| togroup     | - |  必填 | 指定群号 |
| allow     | - |  必填 | 指定是否允许(true,false) |



## 置群员权限_新成员查看历史消息

#### 接口URL
> {{url}}/setgrouppriv_newmembercanviewhistorymsg

#### 请求方式
> POST

#### Content-Type
> urlencoded






#### 请求Body参数

| 参数        | 示例值   | 是否必填   |  参数描述  |
| :--------   | :-----  | :-----  | :----  |
| fromqq     | - |  必填 | 指定框架QQ |
| togroup     | - |  必填 | 指定群号 |
| allow     | - |  必填 | 指定是否允许(true,false) |



## 置群员权限_邀请方式

#### 接口URL
> {{url}}/setgrouppriv_inviteway

#### 请求方式
> POST

#### Content-Type
> urlencoded






#### 请求Body参数

| 参数        | 示例值   | 是否必填   |  参数描述  |
| :--------   | :-----  | :-----  | :----  |
| fromqq     | - |  必填 | 指定框架QQ |
| togroup     | - |  必填 | 指定群号 |
| way     | - |  必填 | 指定方式(1.无需审核;2.需要管理员审核;3.100人以内无需审核) |



## 撤回群聊消息

#### 接口URL
> {{url}}/deletegroupmsg

#### 请求方式
> POST

#### Content-Type
> urlencoded






#### 请求Body参数

| 参数        | 示例值   | 是否必填   |  参数描述  |
| :--------   | :-----  | :-----  | :----  |
| fromqq     | - |  必填 | 指定框架QQ |
| group     | - |  必填 | 指定群号 |
| random     | - |  必填 | 发送消息返回(或事件给出)的random |
| req     | - |  必填 | 发送消息返回(或事件给出)的req |



## 撤回私聊消息

#### 接口URL
> {{url}}/deleteprivatemsg

#### 请求方式
> POST

#### Content-Type
> urlencoded






#### 请求Body参数

| 参数        | 示例值   | 是否必填   |  参数描述  |
| :--------   | :-----  | :-----  | :----  |
| fromqq     | - |  必填 | 指定框架QQ |
| toqq     | - |  必填 | 指定对方QQ |
| random     | - |  必填 | 发送消息返回的random |
| req     | - |  必填 | 发送消息返回的req |
| time     | - |  必填 | 发送消息返回的 |



## 设置位置共享

#### 接口URL
> {{url}}/setsharepos

#### 请求方式
> POST

#### Content-Type
> urlencoded






#### 请求Body参数

| 参数        | 示例值   | 是否必填   |  参数描述  |
| :--------   | :-----  | :-----  | :----  |
| fromqq     | - |  必填 | 指定框架QQ |
| group     | - |  必填 | 指定群号 |
| posx     | - |  必填 | 指定经度 |
| posy     | - |  必填 | 指定纬度 |
| enable     | - |  必填 | 指定是否开启 |



## 上报当前位置

#### 接口URL
> {{url}}/uploadpos

#### 请求方式
> POST

#### Content-Type
> urlencoded






#### 请求Body参数

| 参数        | 示例值   | 是否必填   |  参数描述  |
| :--------   | :-----  | :-----  | :----  |
| fromqq     | - |  必填 | 指定框架QQ |
| group     | - |  必填 | 指定群号 |
| posx     | - |  必填 | 指定经度 |
| posy     | - |  必填 | 指定纬度 |



## 取禁言时间

#### 接口URL
> {{url}}/getmutetime

#### 请求方式
> POST

#### Content-Type
> urlencoded






#### 请求Body参数

| 参数        | 示例值   | 是否必填   |  参数描述  |
| :--------   | :-----  | :-----  | :----  |
| fromqq     | - |  必填 | 指定框架QQ |
| group     | - |  必填 | 指定群号 |



## 处理群验证事件

#### 接口URL
> {{url}}/setgroupaddrequest

#### 请求方式
> POST

#### Content-Type
> urlencoded






#### 请求Body参数

| 参数        | 示例值   | 是否必填   |  参数描述  |
| :--------   | :-----  | :-----  | :----  |
| fromqq     | - |  必填 | 指定框架QQ |
| group     | - |  必填 | 指定群号 |
| qq     | - |  必填 | 指定来源QQ |
| seq     | - |  必填 | 指定seq |
| op     | - |  必填 | 指定处理类型(11同意 12拒绝  14忽略) |
| type     | - |  必填 | 指定事件类型(群事件_某人申请加群:3 群事件_我被邀请加入群:1) |
| reason     | - |  选填 | 拒绝理由 |



## 处理好友验证事件

#### 接口URL
> {{url}}/setfriendaddrequest

#### 请求方式
> POST

#### Content-Type
> urlencoded






#### 请求Body参数

| 参数        | 示例值   | 是否必填   |  参数描述  |
| :--------   | :-----  | :-----  | :----  |
| fromqq     | - |  必填 | 指定框架QQ |
| qq     | - |  必填 | 指定来源QQ |
| seq     | - |  必填 | 指定seq |
| op     | - |  必填 | 指定处理类型(1同意 2拒绝) |



## 上传文件
*注意:本命令会先返回当前HTTP请求 后执行功能
#### 接口URL
> {{url}}/uploadfile

#### 请求方式
> POST

#### Content-Type
> urlencoded






#### 请求Body参数

| 参数        | 示例值   | 是否必填   |  参数描述  |
| :--------   | :-----  | :-----  | :----  |
| fromqq     | - |  必填 | 指定框架QQ |
| group     | - |  必填 | 指定群号 |
| path     | - |  必填 | 指定文件名(存在特殊字符请使用URL编码) |



## 创建群文件夹

#### 接口URL
> {{url}}/newgroupfolder

#### 请求方式
> POST

#### Content-Type
> urlencoded






#### 请求Body参数

| 参数        | 示例值   | 是否必填   |  参数描述  |
| :--------   | :-----  | :-----  | :----  |
| fromqq     | - |  必填 | 指定框架QQ |
| group     | - |  必填 | 指定群号 |
| folder     | - |  必填 | 指定文件夹名称(存在特殊字符请使用URL编码) |



## 重命名群文件夹

#### 接口URL
> {{url}}/renamegroupfolder

#### 请求方式
> POST

#### Content-Type
> urlencoded






#### 请求Body参数

| 参数        | 示例值   | 是否必填   |  参数描述  |
| :--------   | :-----  | :-----  | :----  |
| fromqq     | - |  必填 | 指定框架QQ |
| group     | - |  必填 | 指定群号 |
| folder     | - |  必填 | 指定文件夹名称(存在特殊字符请使用URL编码) |
| name     | - |  必填 | 文件夹新名称(存在特殊字符请使用URL编码) |



## 删除群文件夹

#### 接口URL
> {{url}}/removegroupfolder

#### 请求方式
> POST

#### Content-Type
> urlencoded






#### 请求Body参数

| 参数        | 示例值   | 是否必填   |  参数描述  |
| :--------   | :-----  | :-----  | :----  |
| fromqq     | - |  必填 | 指定框架QQ |
| group     | - |  必填 | 指定群号 |
| folder     | - |  必填 | 指定文件夹名称(存在特殊字符请使用URL编码) |



## 删除群文件

#### 接口URL
> {{url}}/removegroupfile

#### 请求方式
> POST

#### Content-Type
> urlencoded






#### 请求Body参数

| 参数        | 示例值   | 是否必填   |  参数描述  |
| :--------   | :-----  | :-----  | :----  |
| fromqq     | - |  必填 | 指定框架QQ |
| group     | - |  必填 | 指定群号 |
| fileid     | - |  必填 | 指定文件ID |
| filename     | - |  选填 | 指定文件名称(存在特殊字符请使用URL编码) |



## 保存文件到微云

#### 接口URL
> {{url}}/savefiletoweiyun

#### 请求方式
> POST

#### Content-Type
> urlencoded






#### 请求Body参数

| 参数        | 示例值   | 是否必填   |  参数描述  |
| :--------   | :-----  | :-----  | :----  |
| fromqq     | - |  必填 | 指定框架QQ |
| group     | - |  必填 | 指定群号 |
| fileid     | - |  必填 | 指定文件ID |



## 移动群文件

#### 接口URL
> {{url}}/movegroupfile

#### 请求方式
> POST

#### Content-Type
> urlencoded






#### 请求Body参数

| 参数        | 示例值   | 是否必填   |  参数描述  |
| :--------   | :-----  | :-----  | :----  |
| fromqq     | - |  必填 | 指定框架QQ |
| group     | - |  必填 | 指定群号 |
| fileid     | - |  必填 | 指定文件ID |
| fromfolder     | - |  选填 | 当前文件夹名称(存在特殊字符请使用URL编码) |
| tofolder     | - |  选填 | 目标文件夹名称(存在特殊字符请使用URL编码) |



## 取群文件列表

#### 接口URL
> {{url}}/getgroupfilelist

#### 请求方式
> POST

#### Content-Type
> urlencoded






#### 请求Body参数

| 参数        | 示例值   | 是否必填   |  参数描述  |
| :--------   | :-----  | :-----  | :----  |
| fromqq     | - |  必填 | 指定框架QQ |
| group     | - |  必填 | 指定群号 |
| folder     | - |  必填 | 指定文件夹名称(存在特殊字符请使用URL编码) |



## 取群文件下载地址

#### 接口URL
> {{url}}/getgroupfileurl

#### 请求方式
> POST

#### Content-Type
> urlencoded






#### 请求Body参数

| 参数        | 示例值   | 是否必填   |  参数描述  |
| :--------   | :-----  | :-----  | :----  |
| fromqq     | - |  必填 | 指定框架QQ |
| group     | - |  必填 | 指定群号 |
| fileid     | - |  必填 | 指定文件ID |
| filename     | - |  必填 | 指定文件名 |



## 设置在线状态

#### 接口URL
> {{url}}/setonlinestate

#### 请求方式
> POST

#### Content-Type
> urlencoded






#### 请求Body参数

| 参数        | 示例值   | 是否必填   |  参数描述  |
| :--------   | :-----  | :-----  | :----  |
| fromqq     | - |  必填 | 指定框架QQ |
| state     | - |  必填 | 指定在线主状态(11在线 31离开 41隐身 50忙碌 60Q我吧 70请勿打扰) |
| sun     | - |  选填 | [当state=11时]指定在线子状态1(0普通在线 1000我的电量 1011信号弱 1024在线学习 1025在家旅游 1027TiMi中 1016睡觉中 1017游戏中 1018学习中 1019吃饭中 1021煲剧中 1022度假中 1032熬夜中) |
| power     | - |  选填 | [当sun=1000时]自动电量(取值1到100) |



## 发送名片赞

#### 接口URL
> {{url}}/sendlike

#### 请求方式
> POST

#### Content-Type
> urlencoded






#### 请求Body参数

| 参数        | 示例值   | 是否必填   |  参数描述  |
| :--------   | :-----  | :-----  | :----  |
| fromqq     | - |  必填 | 指定框架QQ |
| toqq     | - |  必填 | 指定对方QQ |



## 取图片下载地址

#### 接口URL
> {{url}}/getphotourl

#### 请求方式
> POST

#### Content-Type
> urlencoded






#### 请求Body参数

| 参数        | 示例值   | 是否必填   |  参数描述  |
| :--------   | :-----  | :-----  | :----  |
| photo     | - |  必填 | 指定图片代码(存在特殊字符请使用URL编码) |
| fromqq     | - |  必填 | [群聊图片必填，私聊图片不填]指定框架QQ |
| group     | - |  必填 | [群聊图片必填，私聊图片不填]指定群号 |



## 群文件转发至群

#### 接口URL
> {{url}}/forwardgroupfiletogroup

#### 请求方式
> POST

#### Content-Type
> urlencoded






#### 请求Body参数

| 参数        | 示例值   | 是否必填   |  参数描述  |
| :--------   | :-----  | :-----  | :----  |
| fromqq     | - |  必填 | 指定框架QQ |
| fromgroup     | - |  必填 | 指定来源群 |
| togroup     | - |  必填 | 指定目标群 |
| fileid     | - |  必填 | 指定文件ID(存在特殊字符请使用URL编码) |



## 群文件转发至好友

#### 接口URL
> {{url}}/forwardgroupfiletofriend

#### 请求方式
> POST

#### Content-Type
> urlencoded






#### 请求Body参数

| 参数        | 示例值   | 是否必填   |  参数描述  |
| :--------   | :-----  | :-----  | :----  |
| fromqq     | - |  必填 | 指定框架QQ |
| fromgroup     | - |  必填 | 指定来源群 |
| togroup     | - |  必填 | 指定目标群 |
| fileid     | - |  必填 | 指定文件ID(存在特殊字符请使用URL编码) |
| filename     | - |  必填 | 指定文件名(存在特殊字符请使用URL编码) |
| filesize     | - |  必填 | 指定文件大小 |



## 好友文件转发至好友

#### 接口URL
> {{url}}/forwardfriendfiletofriend

#### 请求方式
> POST

#### Content-Type
> urlencoded






#### 请求Body参数

| 参数        | 示例值   | 是否必填   |  参数描述  |
| :--------   | :-----  | :-----  | :----  |
| logonqq     | - |  必填 | 指定框架QQ |
| fromqq     | - |  必填 | 指定来源QQ |
| toqq     | - |  必填 | 指定目标QQ |
| fileid     | - |  必填 | 指定文件ID(存在特殊字符请使用URL编码) |
| filename     | - |  必填 | 指定文件名(存在特殊字符请使用URL编码) |



## 查看转发聊天记录内容

#### 接口URL
> {{url}}/getforwardedmsg

#### 请求方式
> POST

#### Content-Type
> urlencoded






#### 请求Body参数

| 参数        | 示例值   | 是否必填   |  参数描述  |
| :--------   | :-----  | :-----  | :----  |
| logonqq     | - |  必填 | 指定框架QQ |
| resid     | - |  必填 | 指定resid(xml消息中包含) |



## 查询用户信息

#### 接口URL
> {{url}}/queryuserinfo

#### 请求方式
> POST

#### Content-Type
> urlencoded






#### 请求Body参数

| 参数        | 示例值   | 是否必填   |  参数描述  |
| :--------   | :-----  | :-----  | :----  |
| logonqq     | - |  必填 | 指定框架QQ |
| qq     | - |  必填 | 指定欲查询QQ |



## 查询群信息

#### 接口URL
> {{url}}/querygroupinfo

#### 请求方式
> POST

#### Content-Type
> urlencoded






#### 请求Body参数

| 参数        | 示例值   | 是否必填   |  参数描述  |
| :--------   | :-----  | :-----  | :----  |
| logonqq     | - |  必填 | 指定框架QQ |
| group     | - |  必填 | 指定欲查群号 |



## 发送免费礼物

#### 接口URL
> {{url}}/sendfreepackage

#### 请求方式
> POST

#### Content-Type
> urlencoded






#### 请求Body参数

| 参数        | 示例值   | 是否必填   |  参数描述  |
| :--------   | :-----  | :-----  | :----  |
| fromqq     | - |  必填 | 指定框架QQ |
| group     | - |  必填 | 指定群号 |
| toqq     | - |  必填 | 指定对方QQ |
| pkgid     | - |  必填 | 指定礼物类型(299卡布奇诺;302猫咪手表;280牵你的手;281可爱猫咪;284神秘面具;285甜wink;286我超忙的;289快乐肥宅水;290幸运手链;313坚强;307绒绒手套; 312爱心口罩;308彩虹糖果) |



## 取QQ在线状态

#### 接口URL
> {{url}}/getqqonlinestate

#### 请求方式
> POST

#### Content-Type
> urlencoded






#### 请求Body参数

| 参数        | 示例值   | 是否必填   |  参数描述  |
| :--------   | :-----  | :-----  | :----  |
| logonqq     | - |  必填 | 指定框架QQ |
| qq     | - |  必填 | 指定欲查询QQ |



## 分享音乐

#### 接口URL
> {{url}}/sharemusic

#### 请求方式
> POST

#### Content-Type
> urlencoded






#### 请求Body参数

| 参数        | 示例值   | 是否必填   |  参数描述  |
| :--------   | :-----  | :-----  | :----  |
| logonqq     | - |  必填 | 指定框架QQ |
| totype     | - |  选填 | 指定分享对象类型(0私聊 1群聊  默认0) |
| to     | - |  必填 | 指定分享对象(分享的群或分享的好友QQ) |
| musicname     | - |  必填 | 指定歌曲名(存在特殊字符请使用URL编码) |
| singername     | - |  选填 | 指定歌手名(存在特殊字符请使用URL编码) |
| jumpurl     | - |  必填 | 指定跳转地址(点击音乐json后跳转的地址)(存在特殊字符请使用URL编码) |
| wrapperurl     | - |  必填 | 指定封面地址(音乐的封面图片地址)(存在特殊字符请使用URL编码) |
| fileurl     | - |  必填 | 指定文件地址(音乐源文件地址，如https://xxx.com/xxx.mp3)(存在特殊字符请使用URL编码) |
| apptype     | - |  选填 | 指定应用类型(0QQ音乐 1虾米音乐 2酷我音乐 3酷狗音乐 4网抑云音乐  默认0) |



## 取群未领红包
注意：使用此API获取的红包只能用手Q上"群未领红包"入口的http请求领取
#### 接口URL
> {{url}}/getgrouphb

#### 请求方式
> POST

#### Content-Type
> urlencoded






#### 请求Body参数

| 参数        | 示例值   | 是否必填   |  参数描述  |
| :--------   | :-----  | :-----  | :----  |
| logonqq     | 123456789 |  必填 | 指定框架QQ |
| group     | - |  选填 | 指定群号 |



## 获取skey

#### 接口URL
> {{url}}/getskey

#### 请求方式
> POST

#### Content-Type
> urlencoded






#### 请求Body参数

| 参数        | 示例值   | 是否必填   |  参数描述  |
| :--------   | :-----  | :-----  | :----  |
| logonqq     | - |  必填 | 指定框架QQ |



## 获取pskey

#### 接口URL
> {{url}}/getpskey

#### 请求方式
> POST

#### Content-Type
> urlencoded






#### 请求Body参数

| 参数        | 示例值   | 是否必填   |  参数描述  |
| :--------   | :-----  | :-----  | :----  |
| logonqq     | - |  必填 | 指定框架QQ |
| domain     | - |  必填 | 指定域(tenpay.com;openmobile.qq.com;docs.qq.com;connect.qq.com;qzone.qq.com;vip.qq.com;gamecenter.qq.com;qun.qq.com;game.qq.com;qqweb.qq.com;ti.qq.com;office.qq.com;mail.qq.com;mma.qq.com) |



## 获取clientkey

#### 接口URL
> {{url}}/getclientkey

#### 请求方式
> POST

#### Content-Type
> urlencoded






#### 请求Body参数

| 参数        | 示例值   | 是否必填   |  参数描述  |
| :--------   | :-----  | :-----  | :----  |
| logonqq     | - |  必填 | 指定框架QQ |


