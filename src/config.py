from pydantic_settings import  BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    BASE_URL: str = "http://127.0.0.1:8001"
    DATABASE_URL: str

    USER_JWT_EXP_MIN: int
    USER_JWT_ALG: str
    JWT_SECRET_KEY: str

    SENDER_EMAIL: str
    SENDER_EMAIL_PASSWORD: str

    INVITE_CODE_EXCPIRES_HOURS: int
    INVITE_CODE_SECRET_KEY: str
    INVITE_CODE_SECRET_ALG: str

    RESET_CODE_EXCPIRES_MINUTES: int
    RESET_CODE_SECRET_KEY: str
    RESET_CODE_SECRET_ALG: str

    DEFAULT_PROJECT_ROLE: str = 'USER'

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )

settings = Settings()
