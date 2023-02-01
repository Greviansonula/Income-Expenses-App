from pydantic import BaseSettings, Field

class Settings(BaseSettings):
    db_name: str = Field(..., env="NAME")
    db_user: str = Field(..., env="USER")
    db_user_password: str = Field(..., env="PASSWORD")
    db_host: str = Field(..., env="HOST")
    smtp_server: str = Field(..., env='SMTP_SERVER')
    email_port: int = Field(..., env="EMAIL_PORT")
    sender_email: str = Field(..., env="SENDER_EMAIL")
    email_user_password: str = Field(..., env="EMAIL_USER_PASSWORD")
    secret_key: str = Field(..., env="SECRET_KEY")

    class Config:
        env_file = [".env"]

# @lru_cache
def get_settings():
    return Settings()
    
    
