"""

@FileName: file.py
@Author: chenxiaodong
@CreatTime: 2020/9/17 10:42
@Descriptions: 

"""
import os
from pathlib import Path


class file_tools:
    def __init__(self):
        pass

    def get_current_file_path(self):
        print(Path().resolve())

    @staticmethod
    def get_list_dir():
        return [str(x) for x in Path().iterdir()]

    def check_file_is_exist(self, file_name):
        if file_name in self.get_list_dir():
            return True
        else:
            return False

    @staticmethod
    def mkdir(filepath):
        if Path(filepath).exists():
            return
        else:
            Path(filepath).mkdir()
