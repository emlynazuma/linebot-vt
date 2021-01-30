import logging
import sys
import traceback

from fastapi import FastAPI, Request
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from linebot import LineBotApi, WebhookHandler

from linebot_app.const import api_settings, app_settings
from linebot_app.util import logger


handler = WebhookHandler(app_settings.line_channel_secret)
line_bot_api = LineBotApi(app_settings.line_channel_access_token)


# created fast api instance ######
app = FastAPI(
    title=api_settings.title,
    description=api_settings.description,
    docs_url=api_settings.docs_url,
    redoc_url=api_settings.redoc_url,
    version=api_settings.version,
)


@app.on_event("startup")
async def startup_event():
    """A workaround for gunicorn cannot format access log.

    """
    access_logger = logging.getLogger("gunicorn.access")
    access_handler = logging.FileHandler('/var/log/gunicorn/access.log')
    access_handler.setFormatter(
        logging.Formatter(
            "[%(asctime)s] [%(process)s] [%(levelname)s] %(message)s",
            "%Y-%m-%d %H:%M:%S %z",
        )
    )
    access_logger.addHandler(access_handler)


@app.exception_handler(HTTPException)
async def exception_formatter(request: Request, exc: HTTPException):

    logger.exception(exc.detail)
    return JSONResponse(
        content={"error": exc.detail, "data": None},
        status_code=exc.status_code,
    )


@app.exception_handler(Exception)
async def handle_exception(request: Request, exc: Exception) -> dict:
    logger.exception(str(exc))
    _, _, tb = sys.exc_info()
    summary: traceback.StackSummary = traceback.extract_tb(tb)

    return JSONResponse(
        content={
            "data": None,
            "errors": [{
                "filename": frame.filename,
                "line": frame.line,
                "lineno": frame.lineno,
                "name": frame.name,
            } for frame in summary]
        },
        status_code=500
    )


from linebot_app import events, views
