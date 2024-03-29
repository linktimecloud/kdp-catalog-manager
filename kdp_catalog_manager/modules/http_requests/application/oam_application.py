#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from kdp_catalog_manager.modules.http_requests.base_requests import BaseRequests
from kdp_catalog_manager.common.constants import HTTP_HEADER, RESPONSE_DATA
from kdp_catalog_manager.config.base_config import OAM_BASE_URL, HTTP_TIME_OUT, \
    HTTP_MAX_RETRIES


class OamApplication(BaseRequests):
    def __init__(self, timeout=HTTP_TIME_OUT, max_retries=HTTP_MAX_RETRIES):
        super().__init__(timeout=timeout, max_retries=max_retries)
        self.headers = HTTP_HEADER

    def list_all(self, params=None):
        _url = "{}/api/v1/applications".format(OAM_BASE_URL)
        _response = self.http_request(
            "GET", _url, self.headers, params=params
        )
        return _response.get(RESPONSE_DATA)
