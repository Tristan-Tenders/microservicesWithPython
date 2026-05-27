from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "sqlite:///./activities.db"
    user_service_url: str = "http://localhost:8001"
    game_service_url: str = "http://localhost:8002"

    # Added in Module 4 — RabbitMQ messaging
    rabbitmq_url: str = "amqp://guest:guest@localhost:5672"

    model_config = {"env_file": ".env"}


settings = Settings()
