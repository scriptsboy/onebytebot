# -*- coding:utf-8 -*-

from .config import ConfigManager

ConfigManager().load_zip()
ConfigManager().load_info()
ConfigManager().load_format()
ConfigManager().load_runcode()
ConfigManager().get_bot_username()
