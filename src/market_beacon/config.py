from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings, loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    bitget_api_key: str
    bitget_api_secret: str
    bitget_api_passphrase: str


# Create a singleton instance of the settings
settings = Settings()
