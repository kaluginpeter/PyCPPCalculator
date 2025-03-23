from pydantic import BaseSettings

class Settings(BaseSettings):
    CPP_BACKEND_COMPUTATION: str
    CELERY_NAME: str
    REDIS_BROKER_URL: str
    REDIS_BACKEND_URL: str
    DEFAULT_COMPUTATION_RESULT: str

    class Config:
        env_file = 'backend/.env'

settings = Settings()