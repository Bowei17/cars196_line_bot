import os
import json
import urllib.request, urllib.parse
import requests
from flask import Flask, request, abort
import inference
from io import BytesIO
from PIL import Image

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError, LineBotApiError
)
from linebot.models import (
    MessageEvent, TextMessage, ImageMessage, TextSendMessage, ImageSendMessage,
)
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

app = Flask(__name__)

class Msg():
    def __init__(self, _type, _content ):
        self.type = _type
        self.content = _content


line_bot_api = LineBotApi(os.environ.get("LINEBOT_CHANNEL_ACCESS_TOKEN"))
handler = WebhookHandler(os.environ.get("LINEBOT_CHANNEL_SECRET"))

message_header = {
    'Authorization' : 'Bearer ' + os.environ.get("LINEBOT_CHANNEL_ACCESS_TOKEN")
}

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)

    app.logger.info("Request body: " + body)

    # handle webhook body
    #send(200)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'ok'

@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    # print("event.reply_token:", event.reply_token)
    # print("event.message.text:", event.message.text)
    # print(event)
    returnMsg = Msg("text","")
    # img = Image.open('AM_General_Hummer_SUV_2000.jpg')
    # print(inference.inference(img))

    returnMsg.content = '要傳圖片ㄛ'

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=returnMsg.content)
    )

@handler.add(MessageEvent, message=ImageMessage)
def handle_image_message(event):
    # print("event.reply_token:", event.reply_token)
    # print("event.message.text:", event.message.text)
    # print(event)
    returnMsg = Msg("text","")
    # img = Image.open('AM_General_Hummer_SUV_2000.jpg')
    # print(inference.inference(img))

    message_id = event.message.id
    r = requests.get('https://api-data.line.me/v2/bot/message/'+str(message_id)+'/content', headers=message_header)
    img = Image.open(BytesIO(r.content))
    returnMsg.content = inference.inference(img)

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=returnMsg.content)
    )


if __name__ == '__main__':
    app.run()