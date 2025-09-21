from pydantic_settings import  BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL: str

    USER_JWT_EXP_MIN: int
    USER_JWT_ALG: str
    JWT_SECRET_KEY: str

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )

settings = Settings()
