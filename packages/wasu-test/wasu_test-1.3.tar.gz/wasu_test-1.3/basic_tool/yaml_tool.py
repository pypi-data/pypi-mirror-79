"""

@FileName: yaml_tool.py
@Author: chenxiaodong
@CreatTime: 2020/9/14 16:43
@Descriptions:
This class is for yaml-file deal

"""
import yaml


class yaml_tools:
    def __init__(self, file_path):
        """
        you should provide the file_path to use this tool
        :param: file_path
        :return:None
        """
        self.path = file_path

    def yaml_to_json(self):
        with open(self.path, "r") as f:
            yaml_file = yaml.safe_load(f)
        return yaml_file

    def get_config_by_name(self, config_name):
        """
        use get method to get the String words
        :param:config_name
        :return:String
        """
        return self.yaml_to_json().get(config_name)


