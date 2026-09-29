from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str
    redis_url: str
    gemini_api_key: str = ""
    gemini_model: str = "gemini-3.5-flash"

settings = Settings()