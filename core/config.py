import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):

    MONGODB_URL: str = os.getenv("MONGODB_URL")
    MONGO_DB_NAME: str = os.getenv("MONGO_DB_NAME")
    
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "supersecretkey")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTES", "60"))
    
    STRIPE_SECRET_KEY: str = os.getenv("STRIPE_SECRET_KEY")
    STRIPE_PUBLIC_KEY: str = os.getenv("STRIPE_PUBLIC_KEY")
    # Optional webhook secret for verifying Stripe webhooks
    STRIPE_WEBHOOK_SECRET: str | None = os.getenv("STRIPE_WEBHOOK_SECRET")
    # URLs used for redirects; FRONTEND_URL preferred for full-app deployments
    FRONTEND_URL: str | None = os.getenv("FRONTEND_URL")
    BACKEND_URL: str | None = os.getenv("BACKEND_URL")

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'

settings = Settings()
