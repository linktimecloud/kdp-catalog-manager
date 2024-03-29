#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from unittest import TestCase, mock
from ..oam_application import OamApplication
from kdp_catalog_manager.exceptions.exception import HTTPRequestError


class TestOamApplication(TestCase):
    def setUp(self):
        self.application = OamApplication(1, 2)

    def test_list_all_normal(self):
        with self.assertRaises(HTTPRequestError):
            self.application.list_all()

    def test_list_all_success(self):
        self.rt = {
            "status": 0,
            "message": "ok",
            "data": [
            ]
        }
        self.application.http_request = mock.Mock(return_value=self.rt)
        response = self.application.list_all()
        self.assertEqual(response, [])
