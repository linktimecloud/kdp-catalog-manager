#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/1/19 10:07 上午
import os

import yaml

from kdp_catalog_manager.exceptions.exception import LoadYamlError, \
    FileNotExistsError
from kdp_catalog_manager.utils.log import log


class YAMLUtils(object):
    @staticmethod
    def load_all_yaml(yaml_file_path):
        if not os.path.exists(yaml_file_path):
            raise FileNotExistsError(f"The source yaml file {yaml_file_path} not exists")
        try:
            data = []
            with open(yaml_file_path, 'r') as configfile:
                yaml_file_content = yaml.safe_load_all(configfile)
                for value in yaml_file_content:
                    data.append(value)
            if len(data) == 1:
                return data[0]
            # yaml_file_content's type is dict
            return data
        except Exception as e:
            log.exception(str(e), exc_info=True)
            raise LoadYamlError(e)

    @staticmethod
    def load_yaml(yaml_file_path):
        if not os.path.exists(yaml_file_path):
            raise FileNotExistsError(f"The source yaml file {yaml_file_path} not exists")
        try:
            with open(yaml_file_path, 'r') as configfile:
                yaml_file_content = yaml.safe_load(configfile)
                # yaml_file_content's type is dict
                data = yaml_file_content
            return data
        except Exception as e:
            log.exception(str(e), exc_info=True)
            raise LoadYamlError(e)

    @staticmethod
    def json_to_yaml(json_data, dump_all=True):
        try:
            if not dump_all:
                return yaml.dump(
                    json_data,
                    default_flow_style=False
                )
            return yaml.dump_all(
                json_data,
                default_flow_style=False
            )
        except Exception as e:
            log.exception(str(e), exc_info=True)
            raise

    @staticmethod
    def single_yaml_to_json(yaml_data):
        try:
            _py_object_data = yaml.safe_load(yaml_data)
            return _py_object_data
        except Exception as e:
            log.exception(str(e), exc_info=True)
            raise
