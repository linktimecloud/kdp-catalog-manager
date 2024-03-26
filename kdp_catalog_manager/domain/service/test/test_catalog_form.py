#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from unittest import TestCase

from kdp_catalog_manager.common.constants import CATALOG_FORM_KEY
from kdp_catalog_manager.exceptions.exception import FileNotExistsError, \
    APIRequestedInvalidParamsError
from kdp_catalog_manager.modules.cache.cache import cache_instance
from ..catalog_form import CatalogFormController, CacheNotExistsError, \
    CatalogFormMatchError

TEST_DESC = "Mysql T"


class TestCatalogFormController(TestCase):
    def setUp(self):
        self.catalog_form_metadata = {
            "mysql": {
                "mysql": {
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
            }
        }

        self.catalog_form_data = {
            "apiVersion": "bdc.bdos.io/v1alpha1",
            "kind": "Application"
        }

        self.rt = {
            "mysql": {
                "mysql": {
                    "name": "mysql",
                    "version": "1.0.0",
                    "alias": "mysql",
                    "isGlobal": False,
                    "description": TEST_DESC,
                    "invisible": False,
                    "catalog": "mysql",
                    "dashboardUrl": []
                }
            }
        }

    def set_cache(self):
        cache_instance.set(CATALOG_FORM_KEY, self.catalog_form_metadata)

    def test_get_catalog_form_metadata_from_cache_not_exists(self):
        self.catalog_form_metadata = {}
        self.set_cache()
        try:
            CatalogFormController().get_catalog_form_metadata_for_cache()
        except CacheNotExistsError:
            self.assertEqual(True, True)

    def test_get_catalog_form_metadata_from_cache(self):
        self.set_cache()
        rt = CatalogFormController().get_catalog_form_metadata_for_cache()
        self.assertEqual(rt, self.catalog_form_metadata)

    def test_get_catalog_form_metadata(self):
        self.set_cache()
        rt = CatalogFormController().get_format_catalog_metadata()
        self.assertEqual(rt, self.rt)

    def test_get_catalogs_forms(self):
        self.set_cache()
        rt = CatalogFormController(
            catalog="mysql", app_form="mysql").get_catalogs_forms()
        self.assertEqual(rt, [{
            "name": "mysql", "version": "1.0.0", "alias": 'mysql',
            'invisible': False, 'isGlobal': False,
            'description': TEST_DESC, "catalog": "mysql", 'dashboardUrl': []}])

    def test_get_catalogs_forms_invisible(self):
        self.set_cache()
        rt = CatalogFormController(
            catalog="mysql", app_form="mysql", invisible=True
        ).get_catalogs_forms()
        self.assertEqual(rt, [])

    def test_get_catalogs_form_catalog_not_found_from(self):
        self.set_cache()
        try:
            CatalogFormController(
                catalog="mysql", app_form="spark").get_catalogs_form()
        except CatalogFormMatchError:
            self.assertEqual(True, True)

    def test_get_catalogs_form_invisible(self):
        self.set_cache()
        cache_instance.set("mysql", self.catalog_form_metadata)
        rt = CatalogFormController(
            catalog="mysql", app_form="mysql", invisible=True
        ).get_catalogs_form()
        self.assertEqual(rt, {})
        cache_instance.delete("mysql")

    def test_get_catalogs_form(self):
        self.set_cache()
        cache_instance.set("mysql", self.catalog_form_metadata)
        rt = CatalogFormController(
            catalog="mysql", app_form="mysql").get_catalogs_form()
        self.assertEqual(rt, {
            'name': 'mysql', 'version': '1.0.0', 'alias': 'mysql',
            'isGlobal': False, 'description': 'Mysql T',
            'invisible': False, "catalog": "mysql", 'dashboardUrl': []})
        cache_instance.delete("mysql")

    def test_get_catalog_form_data(self):
        self.set_cache()
        cache_instance.set("mysql-mysql-data", self.catalog_form_data)
        rt = CatalogFormController(
            catalog="mysql", app_form="mysql").get_catalog_form_data()
        self.assertEqual(rt, self.catalog_form_data)

    def test_get_catalog_form_data_not_exists(self):
        self.set_cache()
        cache_instance.set("mysql-mysql-data", self.catalog_form_data)
        rt = CatalogFormController(
            catalog="mysql", app_form="mysql1").get_catalog_form_data()
        self.assertEqual(rt, {})

    def test_get_catalog_form_readme_not_exists(self):
        try:
            CatalogFormController(
                catalog="mysql", app_form="mysql1").get_catalog_form_readme()
        except FileNotExistsError:
            self.assertEqual(True, True)

    def test_get_catalog_form_readme_not_catalog(self):
        try:
            CatalogFormController().get_catalog_form_readme()
        except APIRequestedInvalidParamsError:
            self.assertEqual(True, True)

    def test_get_form_info(self):
        rt = CatalogFormController().get_form_info()
        self.assertEqual(rt, {"mysql": "mysql"})
