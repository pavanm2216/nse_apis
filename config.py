from pydantic_settings import BaseSettings
from pydantic import field_validator


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
    JWT_SECRET: str
    JWT_EXPIRE_MINUTES: int = 60

    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int = 5432
    DB_NAME: str
    DB_SSL: bool = False

    DATABASE_URL: str

    ALLOWED_ORIGINS: str = ""

    @field_validator("JWT_SECRET")
    @classmethod
    def jwt_secret_must_be_strong(cls, v: str) -> str:
        if not v or v in ("changeme", "secret", "your-super-secret-key-change-this"):
            raise ValueError("JWT_SECRET must be set to a strong random value in .env")
        if len(v) < 32:
            raise ValueError("JWT_SECRET must be at least 32 characters")
        return v

    class Config:
        env_file = ".env"


settings = Settings()
