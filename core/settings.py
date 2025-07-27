from pathlib import Path

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).parent.parent


class KafkaSettings(BaseModel):
    uri_server_1: str = "test"


class MyTopicSetting(BaseModel):
    name: str = "messages"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_nested_delimiter="__",
        env_file=BASE_DIR / "core" / ".env"
    )

    kafka: KafkaSettings = KafkaSettings()
    my_topic: MyTopicSetting = MyTopicSetting()


settings = Settings()
