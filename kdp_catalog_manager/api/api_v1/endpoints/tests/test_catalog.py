#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import os.path

from fastapi.testclient import TestClient
from unittest import TestCase
from kdp_catalog_manager.main import app
from kdp_catalog_manager.modules.cache.cache import cache_instance
from kdp_catalog_manager.common.constants import CATALOG_KEY
from kdp_catalog_manager.exceptions.exception import LangNotSupport


class TestCatalogApi(TestCase):
    def setUp(self):
        self.client = TestClient(app=app)
        self.catalog_data = {
            "mysql": {
                "name": "Mysql",
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
        self.catalog_readme_file = "readme/catalog/mysql/i18n/zh/README.html"
        cache_instance.set(CATALOG_KEY, self.catalog_data)
        self.get_catalogs_url = "/api/v1/catalogs"
        self.get_catalogs_mysql_url = "/api/v1/catalogs/mysql"

    def test_get_catalogs(self):
        response = self.client.get(self.get_catalogs_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get("status"), 0)
        catalogs_data = response.json().get("data")
        catalogs_data_keys = catalogs_data[0].keys()
        self.assertEqual(
            list(catalogs_data_keys),
            ["name", "description", "category", "global"]
        )

    def test_get_catalogs_en(self):
        response = self.client.get(
            self.get_catalogs_url, headers={"Accept-Language": "en"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get("status"), 0)
        catalogs_data = response.json().get("data")
        catalogs_data_keys = catalogs_data[0].keys()
        self.assertEqual(
            list(catalogs_data_keys),
            ["name", "description", "category", "global"]
        )

    def test_get_catalogs_not_found_lang(self):
        response = self.client.get(self.get_catalogs_url,
                                   headers={"Accept-Language": "zhs"})
        self.assertEqual(response.json().get("status"), 1)
        self.assertEqual(response.status_code, 200)

    def test_get_catalogs_data_is_None(self):
        self.catalog_data = None
        cache_instance.set(CATALOG_KEY, self.catalog_data)
        response = self.client.get(self.get_catalogs_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get("status"), 1)

    def test_get_catalog(self):
        response = self.client.get(self.get_catalogs_mysql_url)
        self.assertEqual(response.status_code, 200)
        catalogs_data = response.json().get("data")
        catalogs_data_keys = catalogs_data.keys()
        self.assertEqual(
            list(catalogs_data_keys),
            ["name", "description", "category"]
        )

    def test_get_catalog_data_is_None(self):
        self.catalog_data = None
        cache_instance.set(CATALOG_KEY, self.catalog_data)
        response = self.client.get(self.get_catalogs_mysql_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get("status"), 1)

    def test_get_catalog_en(self):
        response = self.client.get(self.get_catalogs_mysql_url,
                                   headers={"Accept-Language": "en"})
        self.assertEqual(response.status_code, 200)
        catalogs_data = response.json().get("data")
        catalogs_data_keys = catalogs_data.keys()
        self.assertEqual(
            list(catalogs_data_keys),
            ["name", "description", "category"]
        )

    def test_get_catalog_not_found_lang(self):
        response = self.client.get(self.get_catalogs_mysql_url,
                                   headers={"Accept-Language": "ens"})
        self.assertEqual(response.status_code, 200)

    def test_catalog_readme(self):
        response = self.client.get("/api/v1/catalogs/mysql/readme")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response.headers.get("content-type"),
            "text/html; charset=utf-8"
        )

    def test_catalog_readme_not_found(self):
        response = self.client.get("/api/v1/catalogs/mysql1/readme")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response.headers.get("content-type"),
            "text/html; charset=utf-8"
        )

    def test_catalog_readme_not_found_lang(self):
        response = self.client.get("/api/v1/catalogs/mysql1/readme",
                                   headers={"Accept-Language": "ens"})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.text,
            "语言不支持:Header Accept-Language is:ens, not in ['zh', 'en']"
        )

    def test_catalog_readme_catalog(self):
        response = self.client.get("/api/v1/catalogs//readme")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response.headers.get("content-type"),
            "application/json"
        )

    def test_catalog_readme_catalog_unsupport_lanf(self):
        try:
            self.client.get("/api/v1/catalogs/mysql/readme",
                                   headers={"Accept-Language": "ens"})
        except LangNotSupport:
            self.assertEqual(True, True)

    def test_catalog_category_zh(self):
        response = self.client.get("/api/v1/catalogs/category/info")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get("status"), 0)
        self.assertEqual(response.json().get("data"), [
            {"category": "系统/大数据开发工具", "sub": [{"name": "mysql", "metadataName": "Mysql", "image": ""}]}])

    def test_catalog_category1_en(self):
        response = self.client.get("/api/v1/catalogs/category/info", headers={"Accept-Language": "en"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get("status"), 0)
        self.assertEqual(response.json().get("data"), [
            {"category": "system.dataManagement", "sub": [{"name": "mysql", "metadataName": "Mysql", "image": ""}]}])

    def test_catalog_global_empty(self):
        response = self.client.get("/api/v1/catalogs/global/info")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get("status"), 0)
        self.assertEqual(response.json().get("data"), [])

    def test_catalog_global_exists(self):
        self.catalog_data["mysql"]["isGlobal"] = True
        cache_instance.set(CATALOG_KEY, self.catalog_data)
        response = self.client.get("/api/v1/catalogs/global/info")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get("status"), 0)
        self.assertEqual(response.json().get("data"), ["mysql"])

    def tearDown(self):
        cache_instance.clear()
