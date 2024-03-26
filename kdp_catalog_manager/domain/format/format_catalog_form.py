#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from kdp_catalog_manager.common.constants import I18N
from kdp_catalog_manager.config.base_config import DEFAULT_LANG
from kdp_catalog_manager.domain.format.base import Format
from kdp_catalog_manager.utils.dictutils import DictUtils
from kdp_catalog_manager.config.base_config import DASHBOARD_URL


class FormatCatalogForm(Format):
    def __init__(self, raw):
        super().__init__(raw)

    def get_version(self):
        return DictUtils().get_items(self.raw, ["version"])

    def get_type(self):
        return DictUtils().get_items(self.raw, ["isGlobal"], False)

    def get_alias(self):
        return DictUtils().get_items(self.raw, ["alias"])

    def get_invisible(self):
        return DictUtils().get_items(self.raw, ["invisible"], False)

    def get_description(self, lang=DEFAULT_LANG):
        if lang == DEFAULT_LANG:
            return DictUtils().get_items(self.raw, ["description"])
        return DictUtils().get_items(
            self.raw, [I18N, lang, "description"])

    def get_dashboard(self, lang=DEFAULT_LANG):
        """
        get catalog from dashboard info
        :param lang:
        :return: [{"name": "xx", "id": "xxx"}]
        """
        dashboard_list = []
        dashboards = DictUtils().get_items(self.raw, ["dashboard"])
        if not dashboards:
            return dashboard_list
        for dashboard in dashboards:
            dashboard_id = DictUtils().get_items(dashboard, ["id"])
            dashboard_name = None
            if lang == DEFAULT_LANG:
                dashboard_name = DictUtils().get_items(
                    dashboard, ["name"])
            if lang != DEFAULT_LANG:
                dashboard_name = DictUtils().get_items(
                    dashboard, [I18N, lang])
            dashboard_list.append({
                "name": dashboard_name,
                "id": dashboard_id,
                "link": f"{DASHBOARD_URL}/d/{dashboard_id}"
            })
        return dashboard_list


def format_catalog_form_metadata(catalog_form_metadatas, filter_lang, filter_invisible):
    catalog_form_metadata_info = {}
    catalog_form_metadata_all = catalog_form_metadatas
    for catalog, catalog_form_metadatas in catalog_form_metadata_all.items():

        catalog_catalog_form_metadatas_info = {}
        for catalog_form, catalog_form_metadata in catalog_form_metadatas.items():

            catalog_form_metadata_format_obj = FormatCatalogForm(
                catalog_form_metadata)
            invisible = catalog_form_metadata_format_obj.get_invisible()
            if filter_invisible != invisible:
                continue
            catalog_catalog_form_metadatas_info[catalog_form] = {
                "name": catalog_form,
                "version": catalog_form_metadata_format_obj.get_version(),
                "alias": catalog_form_metadata_format_obj.get_alias(),
                "invisible": catalog_form_metadata_format_obj.get_invisible(),
                "isGlobal": catalog_form_metadata_format_obj.get_type(),
                "description": catalog_form_metadata_format_obj.get_description(
                    filter_lang),
                "catalog": catalog,
                "dashboardUrl": catalog_form_metadata_format_obj.get_dashboard(
                    filter_lang)
            }
        catalog_form_metadata_info[
            catalog] = catalog_catalog_form_metadatas_info
    return catalog_form_metadata_info
