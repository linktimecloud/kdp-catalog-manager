#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from kdp_catalog_manager.domain.format.format_catalog_runtime_application import \
    format_application
from kdp_catalog_manager.domain.service.catalog_form import \
    CatalogFormController
from kdp_catalog_manager.exceptions.exception import GetDataError, \
    get_exception
from kdp_catalog_manager.modules.http_requests.application.oam_application import \
    OamApplication
from kdp_catalog_manager.utils.log import log


class ApplicationController(object):
    def __init__(self, bdc=None, catalog=None, app_form=None):
        self.bdc = bdc
        self.catalog = catalog
        self.app_form = app_form

    def get_applications(self, label_selector):
        try:
            form_info = CatalogFormController().get_form_info()
        except Exception:
            log.error(get_exception())
            raise GetDataError("get form catalog error")

        params = {}
        if self.bdc:
            params["bdcName"] = self.bdc
        if label_selector:
            params["labelSelector"] = label_selector
        if not params:
            params = None
        all_application = OamApplication().list_all(params)
        applications = format_application(
            all_application, form_info, self.catalog, self.app_form)
        return applications
