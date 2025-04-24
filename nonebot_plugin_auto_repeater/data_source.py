import os

try:
    import ujson as json  # type: ignore
except ModuleNotFoundError as _:
    import json


from nonebot import require

from .config import config

require("nonebot_plugin_localstore")

import nonebot_plugin_localstore as store  # noqa


class Repeater:
    def __init__(self) -> None:
        self.repeat_interval = abs(int(config.repeater_interval))

        self.config_file = store.get_plugin_config_file("config.json")
        self.config: dict[int, bool] = {}
        if os.path.exists(self.config_file):
            self.config = self.read_config()
        else:
            self.write_config()

    def read_config(self) -> dict:
        """读取配置文件"""
        with open(self.config_file, encoding="utf-8") as f:
            self.config = json.load(f)
        return self.config

    def is_enable(self, group_id: int) -> bool:
        """检查群组是否开启复读"""
        return self.config.get(group_id, config.repeater_default_mode)

    def set_mode(self, group_id: int, mode: bool):
        """设置群组复读模式"""
        self.config[group_id] = mode
        self.write_config()

    def write_config(self):
        """写入配置文件"""
        with open(self.config_file, "w", encoding="utf-8") as f:
            json.dump(self.config, f, indent=4)
