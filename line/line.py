# coding:utf-8
# !/usr/bin/python

import google.vision as vision
import json
import os
import vendor.requests as requests

CONTENT_TYPE_TEXT = 1  # Text message
CONTENT_TYPE_IMAGE = 2  # Image message
CONTENT_TYPE_VIDEO = 3  # Video message
CONTENT_TYPE_AUDIO = 4  # Audio message
CONTENT_TYPE_LOCATION = 7  # Location message
CONTENT_TYPE_STICKER = 8  # Sticker message
CONTENT_TYPE_CONTACT = 10  # Contact message

LINE_BOT_API_EVENT = 'https://trialbot-api.line.me/v1/events'
LINE_HEADERS = {
    'Content-type': 'application/json; charset=UTF-8',
    'X-Line-ChannelID': int(os.environ['LineChannelID']),  # Channel ID
    'X-Line-ChannelSecret': os.environ['LineChannelSecret'],  # Channel Secret
    'X-Line-Trusted-User-With-ACL': os.environ['LineTrustedUserWithACL']  # MID (of Channel)
}


def set_return_text(content):
    content_type = content.get("contentType")
    if content_type == CONTENT_TYPE_TEXT:
        content["text"] = u"'" + content.get("text") + u"' ですか、、それは難しい質問ですね。" + os.linesep + \
                          u"写真なら得意ですよ！"
    elif content_type == CONTENT_TYPE_IMAGE:
        image = get_message_content(content)
        content["text"] = vision.get_image_text(image)
    else:
        content["text"] = u"すいません、よくわかりません >_<" + os.linesep + \
                          u"写真なら得意ですよ！"
    content["contentType"] = CONTENT_TYPE_TEXT


def send_to_line(content):
    data = {
        'to': [content.get('from')],
        'toChannel': 1383378250, #FIX
        'eventType': "138311608800106203", #FIX
        'content': content
    };
    r = requests.post(LINE_BOT_API_EVENT, headers=LINE_HEADERS, data=json.dumps(data))
    print(r.content)


def get_message_content(content):
    url = 'https://trialbot-api.line.me/v1/bot/message/%s/content' % content.get("id")
    r = requests.get(url, headers=LINE_HEADERS)
    return r.content
