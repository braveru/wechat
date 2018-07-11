import requests
import itchat
import os


# 在图灵机器人获得回复
def get_response(msg):
    # 图灵机器人的key code
    KEY = '8edce3ce905a4c1dbb965e6b35c3834d'
    apiUrl = 'http://www.tuling123.com/openapi/api'
    data = {
        'key'    : KEY,
        'info'   : msg,
        'userid' : 'wechat-robot',
    }
    try:
        r = requests.post(apiUrl, data=data).json()
        # 字典的get方法在字典没有'text'值的时候会返回None而不会抛出异常
        responseWord = r.get('text')
        print("AI回复内容是：%s" % responseWord)
        return responseWord
    # 为了防止服务器没有正常响应导致程序异常退出，这里用try-except捕获了异常
    # 如果服务器没能正常交互（返回非json或无法连接），那么就会进入下面的return
    except:
        # 将会返回一个None
        return


# 储存聊天记录到TXT文件
def saveAndPrintComments(msg, senderName, groupName=""):
    # 下面是打印信息
    if groupName != "":
        printWord = "群:[%s] | 发件人:[%s] | 新消息:[%s]" % (groupName, senderName, msg)
        saveWord = "%s|%s|%s" % (groupName, senderName, msg)
    else:
        printWord = "个人联系 | 发件人:[%s] | 新消息:[%s]" % (senderName, msg)
        saveWord = "%s|%s|%s" % ("个人联系", senderName, msg)
    print(printWord)

    # 下面是储存Txt文件
    fname = os.getcwd() + "\WeChatMsgList.txt"
    try:
        if os.path.exists(fname):
            fobj = open(fname, 'a')
        else:
            fobj = open(fname, 'w')
    except IOError:
        print('*** file open error:')
    else:
        fobj.write('\n' + saveWord)
        fobj.close()


# 在那些群里面生效
def enableInGroup():
    groupName = [
        "厂妹厂仔",
        "《亲情常在》 幸福常在，快乐永远",
        "TR😜😜😜",
        "SCN PSS team",
        "美女与野兽",
        "大大泡泡糖",
        "致我们还未逝去的青春",
        "红旗飘飘🇨🇳群",
        "有金有银世界杯"
    ]
    return groupName


# 处理群聊消息
@itchat.msg_register(itchat.content.TEXT, isGroupChat=True)
def group_text_reply(msg):
    groupName = enableInGroup()

    # 为了保证在图灵Key出现问题的时候仍旧可以回复，这里设置一个默认回复
    defaultReply = 'I received: ' + msg['Text']

    responseGroupName = msg['User']['NickName']
    senderName = msg['ActualNickName']

    saveAndPrintComments(msg['Text'], senderName, responseGroupName)

    for eachGroupName in groupName:
        if responseGroupName == eachGroupName:
            reply = get_response(msg['Text'])
            return reply or defaultReply


itchat.auto_login(hotReload=True)
itchat.run()
