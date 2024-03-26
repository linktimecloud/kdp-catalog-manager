#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from unittest import TestCase

from kdp_catalog_manager.common.constants import CATALOG_KEY
from kdp_catalog_manager.exceptions.exception import FileNotExistsError, \
    APIRequestedInvalidParamsError
from kdp_catalog_manager.modules.cache.cache import cache_instance
from ..catalog import CatalogController


class TestCatalogController(TestCase):
    def setUp(self):
        self.catalog_data = {
            "mysql": {
                "category": "系统/大数据开发工具",
                "description": "mysql",
                "i18n": {
                    "en": {
                        "category": "system.dataManagement",
                        "description": "mysql"
                    }
                }
            }
        }
        cache_instance.set(CATALOG_KEY, self.catalog_data)

    def test_get_catalog_data_is_None(self):
        self.catalog_data = {"mysql": None}
        cache_instance.set(CATALOG_KEY, self.catalog_data)
        rt = CatalogController(catalog="mysql").get_catalog()
        self.assertEqual(rt, {})

    def test_get_catalog(self):
        self.catalog_data = {"mysql": {}}
        cache_instance.set(CATALOG_KEY, self.catalog_data)
        rt = CatalogController(catalog="mysql").get_catalog()
        self.assertEqual(rt, {})

    def test_get_catalog_readme(self):
        try:
            CatalogController(catalog="mysql", lang="zhs").get_catalog_readme()
        except FileNotExistsError:
            self.assertEqual(True, True)

    def test_get_catalog_readme_catalog_is_None(self):
        try:
            CatalogController(lang="zhs").get_catalog_readme()
        except APIRequestedInvalidParamsError:
            self.assertEqual(True, True)
