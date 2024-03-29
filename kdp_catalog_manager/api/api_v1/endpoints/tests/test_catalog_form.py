#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import os.path

from fastapi.testclient import TestClient
from unittest import TestCase
from kdp_catalog_manager.main import app
from kdp_catalog_manager.modules.cache.cache import cache_instance
from kdp_catalog_manager.common.constants import CATALOG_FORM_KEY
from kdp_catalog_manager.exceptions.exception import KdpCatalogManagerError


class TestCatalogFormApi(TestCase):
    def setUp(self):
        self.client = TestClient(app=app)
        self.catalog_form_metadata = {
            "mysql": {
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
        }
        self.catalog_form_data = {
            "apiVersion": "bdc.bdos.io/v1alpha1",
            "kind": "Application"
        }
        self.catalog_from_readme_file = "readme/form/mysql/i18n/zh/README.html"
        cache_instance.set(CATALOG_FORM_KEY, self.catalog_form_metadata)
        self.get_catalogs_forms_url = "/api/v1/catalogs/mysql/app_forms"
        self.get_catalogs_forms_mysql_url = "/api/v1/catalogs/mysql/app_forms/mysql"
        self.get_catalog_form_mysql_data = "/api/v1/catalogs/mysql/app_forms/mysql/data"
        self.rt_key_list = ["name", "version", "alias", "invisible",
             "isGlobal", "description", "catalog", "dashboardUrl"]

    def test_get_catalogs_froms(self):
        response = self.client.get(self.get_catalogs_forms_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get("status"), 0)
        catalogs_data = response.json().get("data")
        catalogs_data_keys = catalogs_data[0].keys()
        self.assertEqual(
            list(catalogs_data_keys),
            self.rt_key_list
        )

    def test_get_catalogs_forms_en(self):
        response = self.client.get(
            self.get_catalogs_forms_url, headers={"Accept-Language": "en"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get("status"), 0)
        catalogs_data = response.json().get("data")
        catalogs_data_keys = catalogs_data[0].keys()
        self.assertEqual(
            list(catalogs_data_keys),
            self.rt_key_list
        )

    def test_get_catalogs_forms_not_found_lang(self):
        response = self.client.get(self.get_catalogs_forms_url,
                                   headers={"Accept-Language": "zhs"})
        self.assertEqual(response.json().get("status"), 1)
        self.assertEqual(response.status_code, 200)

    def test_get_catalogs_forms_data_is_None(self):
        self.catalog_data = None
        cache_instance.set(CATALOG_FORM_KEY, self.catalog_data)
        response = self.client.get(self.get_catalogs_forms_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get("status"), 1)

    def test_get_catalog_form(self):
        response = self.client.get(self.get_catalogs_forms_mysql_url)
        self.assertEqual(response.status_code, 200)
        catalogs_data = response.json().get("data")
        catalogs_data_keys = catalogs_data.keys()
        self.assertEqual(
            list(catalogs_data_keys),
            self.rt_key_list
        )

    def test_get_catalog_form_data_is_None(self):
        self.catalog_data = None
        cache_instance.set(CATALOG_FORM_KEY, self.catalog_data)
        response = self.client.get(self.get_catalogs_forms_mysql_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get("status"), 1)

    def test_get_catalog_form_en(self):
        response = self.client.get(self.get_catalogs_forms_mysql_url,
                                   headers={"Accept-Language": "en"})
        self.assertEqual(response.status_code, 200)
        catalogs_data = response.json().get("data")
        catalogs_data_keys = catalogs_data.keys()
        self.assertEqual(
            list(catalogs_data_keys),
            self.rt_key_list
        )

    def test_get_catalog_form_not_found_lang(self):
        response = self.client.get(self.get_catalogs_forms_mysql_url,
                                   headers={"Accept-Language": "ens"})
        self.assertEqual(response.status_code, 200)

    def test_get_catalog_form_data(self):
        cache_instance.set("mysql-mysql-data", self.catalog_form_data)
        response = self.client.get(self.get_catalog_form_mysql_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json().get("data"),
            self.catalog_form_data
        )

        # 缓存数据不存在
        cache_instance.delete("mysql-mysql-data")
        response = self.client.get(self.get_catalog_form_mysql_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get("status"), 0)

        # url 异常
        response = self.client.get("/api/v1/catalogs//app_forms//data")
        self.assertEqual(response.status_code, 404)

    def test_catalog_form_readme(self):
        response = self.client.get("/api/v1/catalogs/mysql/app_forms/mysql/readme")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.headers.get("content-type"),
            "text/html; charset=utf-8"
        )

    def test_catalog_form_readme_not_found(self):
        response = self.client.get(
            "/api/v1/catalogs/mysql/app_forms/mysql1/readme",
            headers={"Accept-Language": "zh"})
        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response.headers.get("content-type"),
            "text/html; charset=utf-8"
        )

    def test_catalog_form_readme_not_found_lang(self):
        response = self.client.get(
            "/api/v1/catalogs/mysql/app_forms/mysql/readme",
            headers={"Accept-Language": "ens"})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.text,
            "语言不支持:Header Accept-Language is:ens, not in ['zh', 'en']"
        )

    def test_catalog_form_readme_catalog(self):
        response = self.client.get("/api/v1/catalogs/mysql/app_forms//readme")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response.headers.get("content-type"),
            "application/json"
        )

    def tearDown(self):
        cache_instance.clear()
