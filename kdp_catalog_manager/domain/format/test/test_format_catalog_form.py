#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from unittest import TestCase

from ..format_catalog_form import FormatCatalogForm


TEST_DESC = "mysql test"


class TestFormatCatalogForm(TestCase):
    def setUp(self):
        self.catalog_form_metadata = {
            "version": "1.0.0",
            "alias": "mysql",
            "description": TEST_DESC,
            "isGlobal": False,
            "i18n": {
                "en": {
                    "category": "system.dataManagement",
                    "description": "Mysql M"
                }
            }
        }
        self.dashboard = [{
            "id": "xxx",
            "name": "x1",
            "i18n": {
                "en": "x11"
            }
        }]
        self.catalog_form_format_obj = FormatCatalogForm(self.catalog_form_metadata)

    def test_get_version(self):
        rt = self.catalog_form_format_obj.get_version()
        self.assertEqual(rt, "1.0.0")

    def test_get_version_not_exists(self):
        del self.catalog_form_format_obj.raw["version"]
        rt = self.catalog_form_format_obj.get_version()
        self.assertEqual(rt, None)

    def test_get_type(self):
        rt = self.catalog_form_format_obj.get_type()
        self.assertEqual(rt, False)

    def test_get_type_exists(self):
        self.catalog_form_format_obj.raw["isGlobal"] = True
        rt = self.catalog_form_format_obj.get_type()
        self.assertEqual(rt, True)

    def test_get_alias(self):
        rt = self.catalog_form_format_obj.get_alias()
        self.assertEqual(rt, "mysql")

    def test_get_invisible(self):
        rt = self.catalog_form_format_obj.get_invisible()
        self.assertEqual(rt, False)

    def test_get_invisible_exists(self):
        self.catalog_form_format_obj.raw["invisible"] = True
        rt = self.catalog_form_format_obj.get_invisible()
        self.assertEqual(rt, True)

    def test_get_description(self):
        rt = self.catalog_form_format_obj.get_description()
        self.assertEqual(rt, TEST_DESC)

    def test_get_description_zh(self):
        rt = self.catalog_form_format_obj.get_description("zh")
        self.assertEqual(rt, TEST_DESC)

    def test_get_description_en(self):
        rt = self.catalog_form_format_obj.get_description("en")
        self.assertEqual(rt, "Mysql M")

    def test_dashboard(self):
        rt = self.catalog_form_format_obj.get_dashboard()
        self.assertEqual(rt, [])

    def test_dashboard_exists(self):
        self.catalog_form_format_obj.raw["dashboard"] = self.dashboard
        rt = self.catalog_form_format_obj.get_dashboard()
        self.assertEqual(rt, [{
            "id": "xxx", "name": "x1", 'link': 'https://grafana.com/d/xxx'}])

    def test_dashboard_exists_en(self):
        self.catalog_form_format_obj.raw["dashboard"] = self.dashboard
        rt = self.catalog_form_format_obj.get_dashboard(lang="en")
        self.assertEqual(rt, [{
            "id": "xxx", "name": "x11", 'link': 'https://grafana.com/d/xxx'}])
