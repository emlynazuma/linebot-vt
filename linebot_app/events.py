from urllib.parse import urlparse
from linebot.models import MessageEvent, TextMessage, TextSendMessage, AccountLinkEvent
from linebot_app import app, handler, line_bot_api


def get_account_binding_endpoint():
    path = app.url_path_for("account_binding")
    endpoint = urlparse(line_bot_api.get_webhook_endpoint().endpoint)
    return f"{endpoint.scheme}://{endpoint.netloc}{path}"
    # return "https://account.voicetube.com"


@handler.add(MessageEvent, message=TextMessage)
def handle_message(
    event: MessageEvent
):
    reply = event.message.text
    if event.message.text == "綁定會員":
        endpoint = get_account_binding_endpoint()
        link_token = line_bot_api.issue_link_token(event.source.user_id).link_token
        reply = f"{endpoint}/?linkToken={link_token}"

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(
            text=reply
        )
    )


@handler.add(AccountLinkEvent)
def confirm_account_link(
    event: AccountLinkEvent
):
    if event.link.result == "ok":
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(
                text="account binding success"
            )
        )
    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(
                text="account binding failed"
            )
        )
