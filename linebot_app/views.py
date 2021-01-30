import hashlib
from secrets import token_urlsafe
from typing import Optional

import jwt
from fastapi.exceptions import HTTPException
from fastapi.param_functions import Header
from fastapi.params import Cookie, Query
from linebot.exceptions import InvalidSignatureError
from starlette.requests import Request
from starlette.responses import RedirectResponse, Response

from linebot_app import app, handler
from linebot_app.util import logger


@app.get("/")
def health_check():
    return {"data": "ok"}


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


@app.get("/accountBindingTest")
async def account_binding(
    link_token: str = Query(None, alias="linkToken")
):
    return RedirectResponse(url=f'https://access.line.me/dialog/bot/accountLink?linkToken={link_token}&nonce={token_urlsafe(16)}')


@app.get("/accountBindingRedirect/linkToken/{link_token}")
async def account_redirect(
    link_token: str,
    access_token: Optional[str] = Cookie(None, alias="accessToken"),
):
    nonce = ""
    if access_token:
        encoded = jwt.decode(
            access_token,
            options={
                "verify_signature": False
            },
        )
        user_id = encoded.get("user_id").get("sub")
        nonce = hashlib.sha256(str(user_id).encode()).hexdigest()
    return RedirectResponse(
        url=f'https://access.line.me/dialog/bot/accountLink?linkToken={link_token}&nonce={nonce}'
    )
