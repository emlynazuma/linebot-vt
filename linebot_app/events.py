from urllib.parse import urlparse

from linebot.models.actions import URIAction
from linebot.models.events import AccountLinkEvent, MessageEvent
from linebot.models.messages import TextMessage
from linebot.models.send_messages import TextSendMessage
from linebot.models.template import ButtonsTemplate, TemplateSendMessage

from linebot_app import app_settings, handler, line_bot_api
from linebot_app.util import decrypt, insert_data_to_db

rich_menu_id = "richmenu-c11279f3813d050071852b260237635b"


def redirected_url(link_token):
    redirect_domain = urlparse(
        line_bot_api
        .get_webhook_endpoint()
        .endpoint
    ).netloc
    return f"""https://{redirect_domain}/accountBindingRedirect/{link_token}"""


@handler.add(
    MessageEvent,
    message=TextMessage
)
def handle_message(
    event: MessageEvent
):
    if event.message.text == "綁定會員":
        account_domain = app_settings.account_domain
        link_token = line_bot_api \
            .issue_link_token(event.source.user_id) \
            .link_token
        line_bot_api.reply_message(
            event.reply_token,
            TemplateSendMessage(
                alt_text="會員綁定功能",
                template=ButtonsTemplate(
                    text="綁定會員",
                    actions=[
                        URIAction(
                            label="按此綁定",
                            uri=f"{account_domain}/login?next={redirected_url(link_token)}",
                            type="uri",
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
        line_id = event.source.user_id
        insert_data_to_db(
            (
                "INSERT INTO users (`user_id`, `line_id`, `is_linked`)"
                "VALUES (%(user_id)s, %(line_id)s, %(is_linked)s)"
                "ON DUPLICATE KEY UPDATE `is_linked` = VALUES(is_linked)"
            ),
            [{
                "user_id": decrypt(event.link.nonce),
                "line_id": line_id,
                "is_linked": True,
            }]
        )
        # line_bot_api.link_rich_menu_to_user(
        #     line_id,
        #     rich_menu_id
        # )
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
