from pydantic_settings import  BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL: str

    USER_JWT_EXP_MIN: int
    USER_JWT_ALG: str
    JWT_SECRET_KEY: str

    SENDER_EMAIL: str
    SENDER_EMAIL_PASSWORD: str

    INVITE_CODE_EXCPIRES_HOURS: int
    INVITE_CODE_SECRET_KEY: str
    INVITE_CODE_SECRET_ALG: str

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )

settings = Settings()
