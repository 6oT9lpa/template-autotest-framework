from typing import Any

from pydantic import BaseModel, Field


class CdpCommandConfig(BaseModel):
    name: str
    params: dict[str, Any] = Field(default_factory=dict)


class ChromiumBrowserConfig(BaseModel):
    experimental_options: dict[str, Any] = Field(default_factory=dict)
    cdp_commands: tuple[CdpCommandConfig, ...] = ()


class FirefoxBrowserConfig(BaseModel):
    preferences: dict[str, Any] = Field(default_factory=dict)


class BrowserConfig(BaseModel):
    incognito: bool = False
    arguments: tuple[str, ...] = ()
    chromium: ChromiumBrowserConfig = Field(default_factory=ChromiumBrowserConfig)
    firefox: FirefoxBrowserConfig = Field(default_factory=FirefoxBrowserConfig)
