"""

@FileName: selenium.py
@Author: chenxiaodong
@CreatTime: 2020/9/15 11:01
@Descriptions: 

"""
from pathlib import Path, PurePath

import requests

from selenium import webdriver

from basic_tool.file import file_tools
from basic_tool.yaml import yaml_tools
from schedule.wrappers import singleton


@singleton
class selenium_driver(object):

    def __init__(self, version="", platform="", config_dir="", yaml_file_path="", driver=None):
        self._version = version
        self._platform = platform
        self._config_dir = config_dir
        self._config_file = yaml_file_path
        self._yaml_file = None
        self._driver = driver
        if self._platform == "windows":
            self._driver_path = self._config_dir + "/chromedriver.exe"
        else:
            self._driver_path = self._config_dir + "/chromedriver"

    def get_webdriver_package(self):
        file_tool = file_tools()
        if file_tool.check_file_is_exist(self._config_dir):
            if file_tool.check_file_is_exist(self._driver_path):
                return self._driver_path
            else:
                self._yaml_file = yaml_tools(self._config_dir+"/"+self._config_file)
                url = self._yaml_file.get_config_by_name(
                    "download_url.base_url") + self._version + self._yaml_file.get_config_by_name(self._platform)
                f = requests.get(url)
                with open(self._driver_path, "wb") as file:
                    file.write(f.content)
                return self._driver_path
        else:
            file_tool.mkdir(self._config_dir)

    def start_driver(self):
        self._driver = webdriver.Chrome(executable_path=self.get_webdriver_package())
        self._driver.get(self._yaml_file.get_config_by_name("selenium_url"))
        return self._driver
