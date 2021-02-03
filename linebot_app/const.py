from linebot_app.config import get_api_settings, get_app_settings


api_settings = get_api_settings()
app_settings = get_app_settings()


VOICETUBE_DB_CONFIG = {
    'host': app_settings.db_host,
    'port': app_settings.db_port,
    'database': app_settings.db_database,
    'user': app_settings.db_username,
    'password': app_settings.db_password,
}
