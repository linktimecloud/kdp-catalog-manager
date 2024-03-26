#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from unittest import TestCase
from unittest import mock

from kdp_catalog_manager.exceptions.exception import HTTPRequestError
from kdp_catalog_manager.modules.http_requests.base_requests import BaseRequests, RESPONSE_NOT_FOUND_CODE, APIRequestedURLNotFoundError


class TestHttpRequest(TestCase):
    def setUp(self):
        self.maxDiff = None
        self.header = {"Content-Type": "application/json; charset=UTF-8"}
        self.base_requests = BaseRequests(timeout=1, max_retries=1)

    def test_http_request(self):
        rt = True
        try:
            self.base_requests.http_request(
                "GET", "http://127.0.0.1",
                self.header
            )
        except HTTPRequestError:
            self.assertEqual(rt, True)

    def test_http_request1(self):
        rt = self.base_requests.http_request(
            "GET", "https://wenku.baidu.com/message/getnotice",
            self.header)
        self.assertEqual(rt.get("status").get("code"), 0)
        self.assertEqual(rt, {
            "status": {"code": 0, "msg": "get notice success"},
            "data": {"system": [], "diy": [], "advert": [],
                     "errstr": "get notice success"}
        })

    @mock.patch('httpx.Client')
    def test_http_request_404(self, mock_client):
        mock_response = mock.MagicMock()
        mock_response.status_code = 404
        mock_response.text = "404: Page Not Found"
        mock_client.return_value.__enter__.return_value.request.return_value = mock_response
        with self.assertRaises(HTTPRequestError):
            self.base_requests.http_request(
                "GET", "http://127.0.0.1:8002/api/v1/applicationss",
                self.header)

    @mock.patch('httpx.Client')
    def test_http_request_500(self, mock_client):
        mock_response = mock.MagicMock()
        mock_response.status_code = 500
        with self.assertRaises(HTTPRequestError):
            self.base_requests.http_request(
                "GET", "http://127.0.0.1:8002/api/v1/applicationss",
                self.header)
