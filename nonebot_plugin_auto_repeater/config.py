from nonebot.plugin import get_plugin_config
from pydantic import BaseModel


class Config(BaseModel):
    repeater_interval: int = 300  # 5 * 60S
    repeater_default_mode: bool = True


config = get_plugin_config(Config)
