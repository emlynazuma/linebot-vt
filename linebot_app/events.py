from urllib.parse import urlparse
from linebot.models import MessageEvent, TextMessage, TextSendMessage, AccountLinkEvent
from linebot_app import handler, line_bot_api, app_settings


def binding_url(link_token):
    redirect_domain = urlparse(
        line_bot_api
        .get_webhook_endpoint()
        .endpoint
    ).netloc
    return f"""https://{redirect_domain}/accountBindingRedirect/linkToken/{link_token}"""


@handler.add(
    MessageEvent,
    message=TextMessage
)
def handle_message(
    event: MessageEvent
):
    reply = event.message.text
    if event.message.text == "綁定會員":
        link_token = line_bot_api.issue_link_token(event.source.user_id).link_token
        account_domain = app_settings.account_domain
        reply = f"{account_domain}/login?next={binding_url(link_token)}"

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(
            text=reply
        )
    )


@handler.add(
    AccountLinkEvent
)
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
