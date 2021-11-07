import os
import sys
from argparse import ArgumentParser

from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

# get channel_secret and channel_access_token from your environment variable
channel_secret = os.getenv('LINE_CHANNEL_SECRET', None)
channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', None)
if channel_secret is None:
    print('Specify LINE_CHANNEL_SECRET as environment variable.')
    sys.exit(1)
if channel_access_token is None:
    print('Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.')
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)


@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def message_text(event):
    message_received = event.message.text
    message_send = ""

    if message_received == "ヴィラン":
        message_send = "チャージ満タン、出力30"
    elif message_received == "つらい":
        message_send = "後悔して落ち込んでてもね仕方ないんだよ！ねぇ知ってた！？"
    elif message_received == "文化祭":
        message_send = "だから今年は絶対優勝するの！最後だもん"
    elif message_received == "カワイ子ちゃん":
        message_send = "ムゥー、嫌っ！"
    elif message_received == "あきらめる":
        message_send = "あ、聞いて、知ってる、昔、挫折しちゃってヒーロー諦めちゃって問題起こしちゃった子がいたんだよ、知ってた！？"
    elif message_send == "大変":
        message_send = "大変だよねえ、ちゃんと考えないと辛いよ、これは辛いよー"
    else:
        message_send = "ねぇなんで、「" + message_received + "」って言うの？不思議！"

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=message_send)
    )


if __name__ == "__main__":
    arg_parser = ArgumentParser(
        usage='Usage: python ' + __file__ + ' [--port <port>] [--help]'
    )
    arg_parser.add_argument('-p', '--port', type=int,
                            default=8000, help='port')
    arg_parser.add_argument('-d', '--debug', default=False, help='debug')
    options = arg_parser.parse_args()

    app.run(debug=options.debug, port=options.port)
