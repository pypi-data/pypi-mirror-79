"""

@FileName: yaml_tool.py
@Author: chenxiaodong
@CreatTime: 2020/9/14 16:43
@Descriptions: 

"""
import yaml


class yaml_tools:
    def __init__(self, file_path):
        """
        :@param: file_path
        :@return:

        """
        self.path = file_path

    def yaml_to_json(self):
        with open(self.path, "r") as f:
            yaml_file = yaml.safe_load(f)
        return yaml_file

    def get_config_by_name(self, config_name):
        """
        :param:
        :return:

        """
        return self.yaml_to_json().get(config_name)


