#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import json
from kdp_catalog_manager.utils.log import log


class FormatReturn(object):

    @staticmethod
    def format_return_json(data, status=0, msg="", error_info={}):
        if error_info:
            status = 1
            msg = "BdosException occurred" if msg == "" else msg
            data = None if data is None else data

        rtn = {'status': status, 'data': data,
               'message': msg, "error": error_info}
        return rtn

    @staticmethod
    def format_error_info(
            error_name, raw_exception, app_name=None, func_args=None,
            error_msg=None, exception_type="error"
    ):
        log.error(f"{error_name}: {error_msg}")
        with open("kdp_catalog_manager/exceptions/err_map.json") as fp:
            errors_map_list = json.load(fp)
        error_info = {
            "type": exception_type,
            "exception": raw_exception,
            "args": [] if func_args is None else func_args
        }
        error_data_info = errors_map_list.get(
            error_name,
            errors_map_list.get("KdpCatalogManagerError")
        )
        error_info["info"] = error_data_info
        if error_msg:
            error_info["info"]['description'] = error_msg
        if app_name:
            error_info["app"] = app_name
        else:
            error_info["app"] = error_data_info["app"]
            del error_data_info['app']

        return error_info
