from dataclasses import dataclass, field


@dataclass(frozen=True)
class LoggingConfig:
    enabled: bool = True
    level: str = "INFO"
    console_enabled: bool = True
    file_enabled: bool = True
    file_path: str = "logs/framework.log"
    max_bytes: int = 1_048_576
    backup_count: int = 5
    format: str = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
    date_format: str = "%Y-%m-%d %H:%M:%S"

    @classmethod
    def from_dict(cls, data: dict | None) -> "LoggingConfig":
        if data is None:
            return cls()
        
        return cls(
            enabled=data.get("enabled", cls.enabled),
            level=data.get("level", cls.level),
            console_enabled=data.get("console_enabled", cls.console_enabled),
            file_enabled=data.get("file_enabled", cls.file_enabled),
            file_path=data.get("file_path", cls.file_path),
            max_bytes=data.get("max_bytes", cls.max_bytes),
            backup_count=data.get("backup_count", cls.backup_count),
            format=data.get("format", cls.format),
            date_format=data.get("date_format", cls.date_format),
        )
    
@dataclass(frozen=True)
class Config:
    base_url: str
    browser: str
    incognito: bool
    implicit_wait: int
    explicit_wait: int
    browser_arguments: tuple[str, ...] = field(default_factory=tuple)
    logging: LoggingConfig = field(default_factory=LoggingConfig)

    @classmethod
    def from_dict(cls, data: dict) -> "Config":
        return cls(
            base_url=data["base_url"],
            browser=data["browser"],
            incognito=data["incognito"],
            implicit_wait=data["implicit_wait"],
            explicit_wait=data["explicit_wait"],
            browser_arguments=tuple(data.get("browser_arguments", ())),
            logging=LoggingConfig.from_dict(data.get("logging")),
        )
