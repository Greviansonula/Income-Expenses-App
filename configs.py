from pydantic import BaseSettings, Field
# import os
# from dotenv import load_dotenv

# load_dotenv()

# class Settings():
#     db_name = os.getenv("NAME"),
#     db_user = os.getenv("USER"), 
#     db_user_password = os.getenv("PASSWORD"),
#     db_host = os.getenv("HOST")
#     smtp_server = os.getenv('SMTP_SERVER')
#     email_port = os.getenv("EMAIL_PORT")
#     sender_email = os.getenv("SENDER_EMAIL")
#     email_user_password = os.getenv("EMAIL_USER_PASSWORD")
    
# def get_settings():
#     return Settings()


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
        env_file = [".env", "../.env"]

# @lru_cache
def get_settings():
    return Settings()
    
    
