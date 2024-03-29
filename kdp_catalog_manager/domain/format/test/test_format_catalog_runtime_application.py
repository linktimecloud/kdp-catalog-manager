#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from unittest import TestCase

from ..format_catalog_runtime_application import FormatCatalogRuntimeApplication, format_application


TEST_TIME = "0001-01-01T00:00:00Z"


CATALOG_RUNTIME_APPLICATION = {
  "name": "admin-admin-bdos-file-registry",
  "appFormName": "mysql",
  "appTemplateType": "file-registry",
  "appRuntimeName": "",
  "appRuntimeNs": "admin",
  "bdc": {
    "name": "admin-admin",
    "alias": "",
    "description": "",
    "orgName": "admin",
    "status": ""
  },
  "createTime": TEST_TIME,
  "updateTime": TEST_TIME,
  "labels": {
    "app": "bdos-file-registry",
    "app.core.bdos/type": "system",
    "bdc.bdos.io/name": "admin-admin",
    "bdc.bdos.io/org": "admin"
  },
  "status": "running"
}


class TestFormatCatalogRuntimeApplication(TestCase):
    def setUp(self):
        self.maxDiff = None
        self.catalog_runtime_application_data = CATALOG_RUNTIME_APPLICATION
        self.catalog_runtime_application_format_obj = (
            FormatCatalogRuntimeApplication(
                self.catalog_runtime_application_data
            )
        )

    def test_get_bdc_name(self):
        rt = self.catalog_runtime_application_format_obj.get_bdc_name()
        self.assertEqual(rt, "admin-admin")

    def test_get_bdc_org(self):
        rt = self.catalog_runtime_application_format_obj.get_bdc_org()
        self.assertEqual(rt, "admin")

    def test_get_bdc_status(self):
        rt = self.catalog_runtime_application_format_obj.get_bdc_status()
        self.assertEqual(rt, "")

    def test_get_app_name(self):
        rt = self.catalog_runtime_application_format_obj.get_app_name()
        self.assertEqual(rt, "admin-admin-bdos-file-registry")

    def test_get_app_form(self):
        rt = self.catalog_runtime_application_format_obj.get_app_form()
        self.assertEqual(rt, "mysql")

    def test_get_app_runtime_name(self):
        rt = self.catalog_runtime_application_format_obj.get_app_runtime_name()
        self.assertEqual(rt, "")

    def test_get_app_createtime(self):
        rt = self.catalog_runtime_application_format_obj.get_app_createtime()
        self.assertEqual(rt, TEST_TIME)

    def test_get_app_updatetime(self):
        rt = self.catalog_runtime_application_format_obj.get_app_updatetime()
        self.assertEqual(rt, TEST_TIME)

    def test_get_app_status(self):
        rt = self.catalog_runtime_application_format_obj.get_app_status()
        self.assertEqual(rt, "running")


class TestFormatApplication(TestCase):
    def setUp(self):
        self.maxDiff = None
        self.all_application = CATALOG_RUNTIME_APPLICATION
        self.form_info = {"mysql": "mysql", "spark": "spark"}
        self.filter_catalog = None
        self.filter_form = None

        self.rt = CATALOG_RUNTIME_APPLICATION
        self.add_application = {
            "appFormName": "test",
            "bdc": {
                "name": "",
                "orgName": "admin"
            }
        }

    def test_format_application(self):
        rt = format_application(
            [self.all_application],
            self.form_info,
            self.filter_catalog,
            self.filter_form
        )
        self.assertEqual(rt, [self.rt])

    def test_format_application_not_match_catalog(self):
        rt = format_application(
            [self.all_application, self.add_application],
            self.form_info,
            self.filter_catalog,
            self.filter_form
        )
        self.assertEqual(rt, [self.rt])

    def test_format_application_filter_catalog(self):
        self.add_application["appFormName"] = "spark"
        rt = format_application(
            [self.all_application, self.add_application],
            self.form_info,
            "mysql",
            self.filter_form
        )
        self.assertEqual(rt, [self.rt])

    def test_format_application_filter_catalog1(self):
        self.add_application["appFormName"] = "spark"
        rt = format_application(
            [self.all_application, self.add_application],
            self.form_info,
            "spark",
            self.filter_form
        )
        self.assertEqual(rt, [self.add_application])

    def test_format_application_filter_catalog_form(self):
        self.add_application["appFormName"] = "spark"
        rt = format_application(
            [self.all_application, self.add_application],
            self.form_info,
            self.filter_catalog,
            "mysql"
        )
        self.assertEqual(rt, [self.rt])
