from pydantic import BaseModel, Field, field_validator


class LoggingConfig(BaseModel):
    enabled: bool = True
    level: str = "INFO"
    console_enabled: bool = True
    file_enabled: bool = True
    file_path: str = "logs/framework.log"
    max_bytes: int = Field(
        default=1_048_576,
        gt=0,
    )
    backup_count: int = Field(
        default=5,
        ge=0,
    )

    format: str = (
        "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
    )

    date_format: str = "%Y-%m-%d %H:%M:%S"

    @field_validator("level")
    @classmethod
    def validate_level(cls, value: str) -> str:
        allowed_levels = {
            "INFO",
            "WARNING",
            "ERROR"
        }

        upper_value = value.upper()

        if upper_value not in allowed_levels:
            raise ValueError(
                f"Invalid log level: {value}"
            )

        return upper_value


class Config(BaseModel):
    base_url: str
    browser: str
    implicit_wait: int = Field(ge=0)
    explicit_wait: int = Field(ge=0)
    logging: LoggingConfig = LoggingConfig()

    @field_validator("browser")
    @classmethod
    def validate_browser(cls, value: str) -> str:
        allowed_browsers = {
            "chrome",
            "firefox",
            "edge",
        }

        lower_value = value.lower()

        if lower_value not in allowed_browsers:
            raise ValueError(
                f"Unsupported browser: {value}"
            )

        return lower_value
