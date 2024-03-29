#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import traceback

import httpx

from kdp_catalog_manager.common.constants import RESPONSE_NORMAL_CODE, \
    RESPONSE_NOT_FOUND_CODE
from kdp_catalog_manager.config.base_config import HTTP_TIME_OUT, \
    HTTP_MAX_RETRIES
from kdp_catalog_manager.exceptions.exception import HTTPRequestError, \
    APIRequestedURLNotFoundError
from kdp_catalog_manager.utils.log import log


class BaseRequests(object):
    def __init__(self, timeout=HTTP_TIME_OUT, max_retries=HTTP_MAX_RETRIES):
        self.timeout = timeout
        self.max_retries = max_retries

    def http_request(
            self,
            method,
            url,
            headers,
            data=None,
            params=None
    ):
        try:
            log.info("request url: [{}]{}".format(method, url))
            log.info("request body: {}".format(data))
            log.info("request params: {}".format(params))
            transport = httpx.HTTPTransport(retries=self.max_retries)
            with httpx.Client(transport=transport) as client:
                response = client.request(
                    method,
                    url,
                    headers=headers,
                    params=params,
                    timeout=self.timeout,
                    json=data
                )
                if response.status_code == RESPONSE_NORMAL_CODE:
                    return response.json()
                if response.status_code == RESPONSE_NOT_FOUND_CODE and \
                        response.text == "404: Page Not Found":
                    raise APIRequestedURLNotFoundError()
                else:
                    raise HTTPRequestError(
                        method, url,
                        msg=f"{response.status_code}, response.json()")
        except Exception as e:
            print(traceback.format_exc())
            raise HTTPRequestError(method, url, msg=str(e))
