# -*- coding:utf-8 -*-

import yaml

class Config(object):
    def __init__(self, yml_file_path):
        with open(yml_file_path, 'r', encoding='utf-8') as f:
            self.content = yaml.safe_load(f)

if __name__ == '__main__':
    pass