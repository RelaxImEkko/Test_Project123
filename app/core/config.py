from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+psycopg://postgres:password@db:5432/organizations"
    API_KEY: str = "test-api-key-123"


    class Config:
        env_file = ".env"


settings = Settings()
