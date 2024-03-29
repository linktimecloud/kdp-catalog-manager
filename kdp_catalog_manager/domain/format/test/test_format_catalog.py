#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from unittest import TestCase

from ..format_catalog import FormatCatalog

TEST_SYSTEM_CATEGORY = "系统/大数据开发工具"


class TestFormCatalog(TestCase):
    def setUp(self):
        self.catalog_data = {
            "name": "mysql",
            "category": "系统/大数据开发工具",
            "description": "mysql",
            "i18n": {
                "en": {
                    "category": "system.dataManagement",
                    "description": "Mysql M"
                }
            }
        }
        self.catalog_format_obj = FormatCatalog(self.catalog_data)

    def test_get_name(self):
        rt = self.catalog_format_obj.get_name()
        self.assertEqual(rt, "mysql")

    def test_get_type(self):
        rt = self.catalog_format_obj.get_type()
        self.assertEqual(rt, False)

    def test_get_type_exists(self):
        self.catalog_format_obj.raw["isGlobal"] = True
        rt = self.catalog_format_obj.get_type()
        self.assertEqual(rt, True)

    def test_get_category_default(self):
        rt = self.catalog_format_obj.get_category("zh")
        self.assertEqual(rt, TEST_SYSTEM_CATEGORY)

    def test_get_category_en(self):
        rt = self.catalog_format_obj.get_category("en")
        self.assertEqual(rt, "system.dataManagement")

    def test_get_category(self):
        rt = self.catalog_format_obj.get_category()
        self.assertEqual(rt, TEST_SYSTEM_CATEGORY)

    def test_get_description(self):
        rt = self.catalog_format_obj.get_description()
        self.assertEqual(rt, "mysql")

    def test_get_description_zh(self):
        rt = self.catalog_format_obj.get_description("zh")
        self.assertEqual(rt, "mysql")

    def test_get_description_en(self):
        rt = self.catalog_format_obj.get_description("en")
        self.assertEqual(rt, "Mysql M")
