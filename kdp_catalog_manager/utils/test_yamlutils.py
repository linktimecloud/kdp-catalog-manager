#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import os
from unittest import TestCase
from unittest.mock import patch, mock_open

import yaml
from yaml import SafeLoader

from .yamlutils import YAMLUtils, FileNotExistsError, LoadYamlError


class TestYamlUtils(TestCase):
    def setUp(self):
        self.data = {
            "name": "test",
            "city": {
                "en": "china"
            }
        }
        self.yaml_file = "test.yaml"
        self.yaml_data = yaml.dump(self.data)
        with open(self.yaml_file, "w") as f:
            f.write(yaml.dump(self.data))

    def test_load_all_yaml_many(self):
        self.yaml_data = """---
name: test

---
name: test1"""
        with open(self.yaml_file, "w") as f:
            f.write(self.yaml_data)
        rt = YAMLUtils().load_all_yaml(self.yaml_file)
        self.assertEqual(rt, [{"name": "test"}, {"name": "test1"}])

    def test_load_all_yaml(self):
        with open(self.yaml_file, "w") as f:
            f.write(self.yaml_data)
        rt = YAMLUtils().load_all_yaml(self.yaml_file)
        self.assertEqual(rt, self.data)

    @patch('os.path.exists', return_value=False)
    def test_load_all_yaml_non_existing_file(self, mock_exists):
        with self.assertRaises(FileNotExistsError):
            YAMLUtils.load_all_yaml('t.yaml')

    @patch('builtins.open', side_effect=Exception)
    @patch('os.path.exists', return_value=True)
    def test_load_all_yaml_exception_handling(self, mock_exists, mock_open):
        with self.assertRaises(LoadYamlError):
            YAMLUtils.load_all_yaml(self.yaml_file)

    def test_load_yaml(self):
        rt = YAMLUtils().load_yaml(self.yaml_file)
        self.assertEqual(rt, self.data)

    def test_load_yaml_non_existing_file(self):
        with self.assertRaises(FileNotExistsError):
            YAMLUtils().load_yaml("tt.yaml")

    def test_load_yaml_err(self):
        err_log_file = "err.log"
        self.yaml_data = """name: -"""
        with open(err_log_file, "w") as f:
            f.write(self.yaml_data)
        with self.assertRaises(LoadYamlError):
            YAMLUtils().load_yaml(err_log_file)
        os.remove(err_log_file)

    @patch('yaml.dump_all')
    def test_json_to_yaml(self, mock_dump_all):
        YAMLUtils().json_to_yaml(self.data)
        mock_dump_all.assert_called_once_with(
            self.data, default_flow_style=False)

    @patch('yaml.dump')
    def test_json_to_yaml_single(self, mock_dump):
        YAMLUtils().json_to_yaml(self.data, dump_all=False)
        mock_dump.assert_called_once_with(self.data, default_flow_style=False)

    @patch('yaml.load')
    def test_yaml_to_json_single(self, mock_load_all):
        YAMLUtils().single_yaml_to_json(self.yaml_data)
        mock_load_all.assert_called_once_with(
            self.yaml_data,
            SafeLoader
        )

    def tearDown(self):
        os.remove(self.yaml_file)
