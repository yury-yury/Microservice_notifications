from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    The Settings class inherits from the parent BaseSettings class from the pydantic_settings module.
    Contains the necessary settings for working with the database, with the SMTP.server and application.
    """

    server_host: str = "0.0.0.0"
    server_port: int = 8000

    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_COLLECTION: str

    EMAIL: str
    SMTP_HOST: str
    SMTP_PORT: int
    SMTP_LOGIN: str
    SMTP_PASSWORD: str
    SMTP_EMAIL: str
    SMTP_NAME: str

    @property
    def DATABASE_URL(self) -> str:
        """
        The DATABASE_URL function is a property argument of the Settings class.
        When accessed, returns the DSN for the database connection as a string.
        """
        return f"mongodb://{self.DB_HOST}:{self.DB_PORT}/"

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings(_env_file=".env", _env_file_encoding="utf-8")
