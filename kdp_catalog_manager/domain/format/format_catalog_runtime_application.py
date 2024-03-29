#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from kdp_catalog_manager.domain.format.base import Format
from kdp_catalog_manager.utils.dictutils import DictUtils
from kdp_catalog_manager.utils.log import log


class FormatCatalogRuntimeApplication(Format):
    def __init__(self, raw):
        super().__init__(raw)

    def get_bdc_name(self):
        return DictUtils().get_items(self.raw, ["bdc", "name"])

    def get_bdc_org(self):
        return DictUtils().get_items(self.raw, ["bdc", "orgName"])

    def get_bdc_status(self):
        return DictUtils().get_items(self.raw, ["bdc", "status"])

    def get_app_name(self):
        return DictUtils().get_items(self.raw, ["name"])

    def get_app_form(self):
        return DictUtils().get_items(self.raw, ["appFormName"])

    def get_app_runtime_name(self):
        return DictUtils().get_items(self.raw, ["appRuntimeName"])

    def get_app_createtime(self):
        return DictUtils().get_items(self.raw, ["createTime"])

    def get_app_updatetime(self):
        return DictUtils().get_items(self.raw, ["updateTime"])

    def get_app_status(self):
        return DictUtils().get_items(self.raw, ["status"])


def format_application(
        all_application,
        form_info,
        filter_catalog,
        filter_form
):
    applications = []
    # deal with get application data is empty list or None
    if not all_application:
        return applications
    for application_data in all_application:
        application = application_data
        application_format_obj = (
            FormatCatalogRuntimeApplication(application))
        application_form = application_format_obj.get_app_form()
        application_catalog = DictUtils().get_items(
            form_info, [application_form])

        if not application_catalog:
            log.warning(f"{application_form} not match catalog, "
                        f"get data is {application_catalog}")
            continue

        # filter application
        if filter_catalog and filter_catalog != application_catalog:
            continue
        if filter_form and filter_form != application_form:
            continue

        application["catalog"] = application_catalog
        applications.append(application)
    return applications
