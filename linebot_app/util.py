import logging
import os
from urllib.request import Request, urlopen

from fastapi import Header, HTTPException

logging.basicConfig(
    format='[%(asctime)s] %(levelname)s: %(message)s',
    datefmt='%m/%d/%Y %I:%M:%S %p',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

config = {
    'host': os.environ['DB_HOST'],
    'port': int(os.environ['DB_PORT']),
    'database': os.environ['DB_DATABASE'],
    'user': os.environ['DB_USERNAME'],
    'password': os.environ['DB_PASSWORD']
}


def check_token(token):
    url = f'{os.environ["AUTH_DOMAIN"]}/accessTokens'
    headers = {'Authorization': f'Bearer {token}'}
    return urlopen(Request(url, headers=headers), timeout=5)


async def voicetube_authenticate(bearer: str = Header(..., alias="Authorization")):
    token = bearer.split(' ')[1]
    try:
        res = check_token(token)
    except Exception:
        raise HTTPException(status_code=400, detail="Authorization header invalid")

    if res.code != 200:
        raise HTTPException(status_code=400, detail=f"Authentication failed: {res}', res.code")


async def apikey_verification(apikey: str = Header(...)):
    if apikey != os.environ['APIKEY']:
        raise HTTPException(status_code=400, detail="Authorization header invalid")
