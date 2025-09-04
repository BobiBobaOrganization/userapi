from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    APPLICATION_VERSION: str = "test"
    TEST_MODE: bool = False
    DATABASE_URL: str = "unset" if TEST_MODE else None
    DATABASE_SCHEMA: str = "public"

    model_config = SettingsConfigDict(env_file=".env")

def get_settings():
    return Settings()