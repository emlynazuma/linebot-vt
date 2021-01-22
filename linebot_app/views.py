import json

from fastapi.exceptions import HTTPException
from fastapi.param_functions import Body, Header
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from starlette.requests import Request

from linebot_app import app, app_settings
from linebot_app.util import logger


line_bot_api = LineBotApi(app_settings.line_channel_access_token)
handler = WebhookHandler(app_settings.line_channel_secret)


@app.get("/")
def health_check():
    return "ok"


@app.post("/callback")
async def callback(
    request: Request,
    signature: str = Header(..., alias="X-Line-Signature"),
):
    body = await request.body()
    body = body.decode()
    logger.info(f"Request body: {body}")
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        logger.warning("Invalid signature. Please check your channel access token/channel secret.")
        raise HTTPException(400, "Invalid signature.")

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(
    event: MessageEvent
):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))
