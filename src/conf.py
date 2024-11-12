from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_NAME: str


settings = Settings()


if __name__ == "__main__":
    print(settings.DB_NAME)
