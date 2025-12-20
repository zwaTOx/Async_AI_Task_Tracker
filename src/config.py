from pydantic_settings import  BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    BASE_URL: str = "http://127.0.0.1:8001"
    DATABASE_URL: str

    UPLOAD_DIRECTORY: str
    MAX_FILE_SIZE_MB: int = 50*1024*1024
    ALLOWED_ICON_TYPES: list[str] = ["image/jpeg", "image/png"]
    ALLOWED_FILE_TYPES: list[str] = ["image/jpeg", "image/png", "application/pdf", "text/csv", 
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        "application/vnd.ms-excel"]

    USER_JWT_EXP_MIN: int
    USER_JWT_ALG: str
    JWT_SECRET_KEY: str

    SENDER_EMAIL: str
    SENDER_EMAIL_PASSWORD: str

    INVITE_CODE_EXCPIRES_HOURS: int = 24
    INVITE_CODE_SECRET_KEY: str
    INVITE_CODE_SECRET_ALG: str

    RESET_CODE_EXCPIRES_MINUTES: int = 5
    RESET_CODE_SECRET_KEY: str
    RESET_CODE_SECRET_ALG: str

    DEFAULT_PROJECT_ROLE: str = 'USER'
    
    NOTIF_DEFAULT_LIMIT: int = 10

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )

settings = Settings()
