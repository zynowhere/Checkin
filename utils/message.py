# -*- coding: utf-8 -*-
import base64
import hashlib
import hmac
import json
import time
import urllib.parse

import requests


def message2server(sckey, content):
    print("server 酱推送开始")
    data = {"text": "每日签到", "desp": content.replace("\n", "\n\n")}
    requests.post(url=f"https://sc.ftqq.com/{sckey}.send", data=data)
    return


def message2server_turbo(sendkey, content):
    print("server 酱 Turbo 推送开始")
    data = {"text": "每日签到", "desp": content.replace("\n", "\n\n")}
    requests.post(url=f"https://sctapi.ftqq.com/{sendkey}.send", data=data)
    return


def message2coolpush(
    coolpushskey, content, coolpushqq: bool = True, coolpushwx: bool = False, coolpushemail: bool = False
):
    print("Cool Push 推送开始")
    params = {"c": content, "t": "每日签到"}
    if coolpushqq:
        requests.post(url=f"https://push.xuthus.cc/send/{coolpushskey}", params=params)
    if coolpushwx:
        requests.post(url=f"https://push.xuthus.cc/wx/{coolpushskey}", params=params)
    if coolpushemail:
        requests.post(url=f"https://push.xuthus.cc/email/{coolpushskey}", params=params)
    return


def message2qmsg(qmsg_key, qmsg_type, content):
    print("qmsg 酱推送开始")
    params = {"msg": content}
    if qmsg_type == "group":
        requests.get(url=f"https://qmsg.zendee.cn/group/{qmsg_key}", params=params)
    else:
        requests.get(url=f"https://qmsg.zendee.cn/send/{qmsg_key}", params=params)
    return


def message2telegram(tg_api_host, tg_proxy, tg_bot_token, tg_user_id, content):
    print("Telegram 推送开始")
    send_data = {"chat_id": tg_user_id, "text": content, "disable_web_page_preview": "true"}
    if tg_api_host:
        url = f"https://{tg_api_host}/bot{tg_bot_token}/sendMessage"
    else:
        url = f"https://api.telegram.org/bot{tg_bot_token}/sendMessage"
    if tg_proxy:
        proxies = {
            "http": tg_proxy,
            "https": tg_proxy,
        }
    else:
        proxies = None
    requests.post(url=url, data=send_data, proxies=proxies)
    return


def message2dingtalk(dingtalk_secret, dingtalk_access_token, content):
    print("Dingtalk 推送开始")
    timestamp = str(round(time.time() * 1000))
    secret_enc = dingtalk_secret.encode("utf-8")
    string_to_sign = "{}\n{}".format(timestamp, dingtalk_secret)
    string_to_sign_enc = string_to_sign.encode("utf-8")
    hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
    sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
    send_data = {"msgtype": "text", "text": {"content": content}}
    requests.post(
        url="https://oapi.dingtalk.com/robot/send?access_token={0}&timestamp={1}&sign={2}".format(
            dingtalk_access_token, timestamp, sign
        ),
        headers={"Content-Type": "application/json", "Charset": "UTF-8"},
        data=json.dumps(send_data),
    )
    return


def message2bark(bark_url: str, content):
    print("Bark 推送开始")
    if not bark_url.endswith("/"):
        bark_url += "/"
    url = f"{bark_url}{content}"
    headers = {"Content-type": "application/x-www-form-urlencoded"}
    requests.get(url=url, headers=headers)
    return


def message2qywxrobot(qywx_key, content):
    print("企业微信群机器人推送开始")
    requests.post(
        url=f"https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key={qywx_key}",
        data=json.dumps({"msgtype": "text", "text": {"content": content}}),
    )
    return


def message2qywxapp(qywx_corpid, qywx_agentid, qywx_corpsecret, qywx_touser, content):
    print("企业微信应用消息推送开始")
    res = requests.get(
        f"https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={qywx_corpid}&corpsecret={qywx_corpsecret}"
    )
    token = res.json().get("access_token", False)
    data = {
        "touser": qywx_touser,
        "agentid": qywx_agentid,
        "msgtype": "textcard",
        "textcard": {
            "title": "签到通知",
            "description": content,
            "url": "https://github.com/Sitoi/dailycheckin",
            "btntxt": "开源项目",
        },
    }
    requests.post(url=f"https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={token}", data=json.dumps(data))
    return


def message2pushplus(pushplus_token, content, pushplus_topic=None):
    print("Pushplus 推送开始")
    data = {"token": pushplus_token, "title": "签到通知", "content": content.replace("\n", "<br>"), "template": "json"}
    if pushplus_topic:
        data["topic"] = pushplus_topic
    requests.post(url=f"http://www.pushplus.plus/send", data=json.dumps(data))
    return


def important_notice():
    datas = requests.get(url="https://api.github.com/repos/Sitoi/dailycheckin/issues?state=open&labels=通知").json()
    if datas:
        data = datas[0]
        title = data.get("title")
        body = data.get("body")
        url = data.get("html_url")
        notice = f"重要通知: {title}\n通知内容: {body}\n详细地址: {url}"
    else:
        notice = None
    return notice


def push_message(content_list: list, notice_info: dict):
    dingtalk_secret = notice_info.get("dingtalk_secret")
    dingtalk_access_token = notice_info.get("dingtalk_access_token")
    bark_url = notice_info.get("bark_url")
    sckey = notice_info.get("sckey")
    sendkey = notice_info.get("sendkey")
    qmsg_key = notice_info.get("qmsg_key")
    qmsg_type = notice_info.get("qmsg_type")
    tg_bot_token = notice_info.get("tg_bot_token")
    tg_user_id = notice_info.get("tg_user_id")
    tg_api_host = notice_info.get("tg_api_host")
    tg_proxy = notice_info.get("tg_proxy")
    coolpushskey = notice_info.get("coolpushskey")
    coolpushqq = notice_info.get("coolpushqq")
    coolpushwx = notice_info.get("coolpushwx")
    coolpushemail = notice_info.get("coolpushemail")
    qywx_key = notice_info.get("qywx_key")
    qywx_corpid = notice_info.get("qywx_corpid")
    qywx_agentid = notice_info.get("qywx_agentid")
    qywx_corpsecret = notice_info.get("qywx_corpsecret")
    qywx_touser = notice_info.get("qywx_touser")
    pushplus_token = notice_info.get("pushplus_token")
    pushplus_topic = notice_info.get("pushplus_topic")
    content_str = "\n-----------------------------\n\n".join(content_list)
    message_list = [content_str]
    try:
        notice = important_notice()
        if notice:
            message_list.append(notice)
            content_list.append(notice)
    except Exception as e:
        print("获取重要通知失败:", e)
    for content in content_list:
        if qmsg_key:
            try:
                message2qmsg(qmsg_key=qmsg_key, qmsg_type=qmsg_type, content=content)
            except Exception as e:
                print("qmsg 推送失败", e)
        if coolpushskey:
            try:
                message2coolpush(
                    coolpushskey=coolpushskey,
                    coolpushqq=coolpushqq,
                    coolpushwx=coolpushwx,
                    coolpushemail=coolpushemail,
                    content=content,
                )
            except Exception as e:
                print("coolpush 推送失败", e)
        if qywx_touser and qywx_corpid and qywx_corpsecret and qywx_agentid:
            try:
                message2qywxapp(
                    qywx_corpid=qywx_corpid,
                    qywx_agentid=qywx_agentid,
                    qywx_corpsecret=qywx_corpsecret,
                    qywx_touser=qywx_touser,
                    content=content,
                )
            except Exception as e:
                print("企业微信应用消息推送失败", e)
    for message in message_list:
        if dingtalk_access_token and dingtalk_secret:
            try:
                message2dingtalk(
                    dingtalk_secret=dingtalk_secret, dingtalk_access_token=dingtalk_access_token, content=message
                )
            except Exception as e:
                print("钉钉推送失败", e)
        if sckey:
            try:
                message2server(sckey=sckey, content=message)
            except Exception as e:
                print("Server 推送失败", e)
        if sendkey:
            try:
                message2server_turbo(sendkey=sendkey, content=message)
            except Exception as e:
                print("Server Turbo 推送失败", e)
        if bark_url:
            try:
                message2bark(bark_url=bark_url, content=message)
            except Exception as e:
                print("Bark 推送失败", e)
        if qywx_key:
            try:
                message2qywxrobot(qywx_key=qywx_key, content=message)
            except Exception as e:
                print("企业微信群机器人推送失败", e)
        if pushplus_token:
            try:
                message2pushplus(pushplus_token=pushplus_token, content=message, pushplus_topic=pushplus_topic)
            except Exception as e:
                print("Pushplus 推送失败", e)
        if tg_user_id and tg_bot_token:
            try:
                message2telegram(
                    tg_api_host=tg_api_host,
                    tg_proxy=tg_proxy,
                    tg_user_id=tg_user_id,
                    tg_bot_token=tg_bot_token,
                    content=message,
                )
            except Exception as e:
                print("Telegram 推送失败", e)


if __name__ == "__main__":
    print(important_notice())
