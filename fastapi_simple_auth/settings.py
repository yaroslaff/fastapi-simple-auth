from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    db_url: str = ""

    app_title: str = "My Noname App"
    secret_key: str = None

    login_result: str = "session"
    email_verification: bool = False
    
    username_is_email: bool = True

    code_size: int = 6
    code_set: str = "digits"
    code_lifetime: int = 86400
    code_regenerate: int = 0
    
    mail_transport: str = "stdout"
    mail_host: str = "127.0.0.1"
    mail_port: int = 25
    mail_from: str = "NoReply <noreply@example.com>"
    mail_user: str = None
    mail_password: str = None
    mail_starttls: bool = False

    auth_transport: str = "session"

    afterlogin_url: str = "/"
    afterlogout_url: str = "login"
    notauth_login: bool = False


    model_config = SettingsConfigDict(env_file=".env", extra='ignore')

settings = Settings()