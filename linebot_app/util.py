import logging

import mysql.connector
from cryptography.fernet import Fernet

from linebot_app import app_settings
from linebot_app.const import VOICETUBE_DB_CONFIG

logging.basicConfig(
    format='[%(asctime)s] %(levelname)s: %(message)s',
    datefmt='%m/%d/%Y %I:%M:%S %p',
    level=logging.INFO
)

logger = logging.getLogger(__name__)


def encrypt(plaintext):
    return Fernet(app_settings.encrypt_key) \
        .encrypt(plaintext.encode()) \
        .decode()


def decrypt(ciphertext):
    return Fernet(app_settings.encrypt_key) \
        .decrypt(ciphertext.encode()) \
        .decode()


def insert_data_to_db(statement: str, data: list):
    """Inserts data to database.

    Args:
        statement (str): The statement of the insertion.
        data (list, optional): [description]. The data to be inserted. Must be list of tupples or dictionaries.
    """
    cnx = mysql.connector.connect(**VOICETUBE_DB_CONFIG)
    cursor = cnx.cursor()
    cursor.executemany(statement, data)
    cnx.commit()
    cursor.close()
    cnx.close()
