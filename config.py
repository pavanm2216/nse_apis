from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    NSE_LOGIN_USER_ID: str = ""
    NSE_API_SECRET: str = ""
    NSE_API_LICENSE_KEY: str = ""
    NSE_MEMBER_CODE: str = ""
    NSE_MEMBER_ID: str = ""
    NSE_BASE_URL: str = "https://nseinvestuat.nseindia.com"
    NSE_PROXY: str = ""

    APP_USERNAME: str = ""
    APP_PASSWORD: str = ""
    JWT_SECRET: str = "changeme"
    JWT_EXPIRE_MINUTES: int = 60

    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int = 5432
    DB_NAME: str
    DB_SSL: bool = False

    DATABASE_URL: str

    class Config:
        env_file = ".env"

settings = Settings()
