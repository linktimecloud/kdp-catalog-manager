#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import os
from unittest import TestCase
from unittest.mock import patch, mock_open

from kdp_catalog_manager.exceptions.exception import FileNotExistsError, \
    ReadFileError, WriteFileError
from .fileutils import FileUtils


class TestFileUtils(TestCase):
    def setUp(self):
        self.file = "test.log"
        with open(self.file, "a") as f:
            f.write("test")

    def test_check_file_exists(self):
        # 测试文件是否存在的情况
        with patch('os.path.lexists') as mock_lexists:
            mock_lexists.return_value = True
            self.assertTrue(FileUtils.check_file_exists(self.file))

        # 测试文件不存在的情况
        with patch('os.path.lexists') as mock_lexists:
            mock_lexists.return_value = False
            self.assertFalse(FileUtils.check_file_exists('a.log'))

    @patch('builtins.open', new_callable=mock_open, read_data='test')
    def test_read_file(self, mock_open):
        # 测试文件已存在
        rt = FileUtils().read_file(self.file)
        self.assertEqual(rt, "test")

        # 测试读取不存在的文件的情况
        with self.assertRaises(FileNotExistsError):
            FileUtils().read_file("a.log")

        # 测试读取文件时发生IOError的情况
        with patch('builtins.open', side_effect=IOError):
            with self.assertRaises(ReadFileError):
                FileUtils().read_file(self.file)

    @patch('builtins.open', new_callable=mock_open)
    def test_write_file(self, mock_open):
        FileUtils().write_file("test1", self.file)

        # 测试写文件时发生IOError的情况
        with patch('builtins.open', side_effect=IOError):
            with self.assertRaises(WriteFileError):
                FileUtils().write_file("test1", self.file)

    def tearDown(self):
        os.remove(self.file)
