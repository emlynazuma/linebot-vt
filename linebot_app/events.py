from urllib.parse import urlparse

from linebot.models import (AccountLinkEvent, ButtonsTemplate, MessageEvent,
                            TemplateSendMessage, TextMessage, TextSendMessage)
from linebot.models.actions import URIAction

from linebot_app import app_settings, handler, line_bot_api


def redirected_url(link_token):
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
    if event.message.text == "綁定會員":
        link_token = line_bot_api.issue_link_token(event.source.user_id).link_token
        account_domain = app_settings.account_domain

        line_bot_api.reply_message(
            event.reply_token,
            TemplateSendMessage(
                alt_text="會員綁定功能",
                template=ButtonsTemplate(
                    text="綁定會員",
                    actions=[
                        URIAction(
                            label="按此綁定",
                            uri=f"{account_domain}/login?next={redirected_url(link_token)}"
                        )
                    ]
                )
            )
        )
    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(
                text=event.message.text
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
