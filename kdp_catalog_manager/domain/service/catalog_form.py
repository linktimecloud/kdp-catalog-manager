#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import os

from kdp_catalog_manager.common.constants import CATALOG_FORM_KEY, \
    CATALOG_FROM_DATA_KEY, I18N, README_HTML
from kdp_catalog_manager.config.base_config import DEFAULT_LANG, \
    CATALOG_FROM_README_DIR
from kdp_catalog_manager.domain.format.format_catalog_form import \
    FormatCatalogForm, format_catalog_form_metadata
from kdp_catalog_manager.exceptions.exception import CacheNotExistsError, \
    CatalogFormMatchError, APIRequestedInvalidParamsError
from kdp_catalog_manager.modules.cache.cache import cache_instance
from kdp_catalog_manager.utils.dictutils import DictUtils
from kdp_catalog_manager.utils.fileutils import FileUtils
from kdp_catalog_manager.modules.http_requests.application.oam_application import OamApplication
from kdp_catalog_manager.domain.format.format_catalog_runtime_application import FormatCatalogRuntimeApplication
from kdp_catalog_manager.utils.log import log


class CatalogFormController(object):
    def __init__(
            self, catalog=None, app_form=None,
            lang=DEFAULT_LANG, invisible=False
    ):
        self.catalog = catalog
        self.app_form = app_form
        self.lang = lang
        self.invisible = invisible

    def get_catalog_form_metadata_for_cache(self):
        """
        get catalog from metadata from cache
        :return:
        """
        catalog_form_metadatas = cache_instance.get(CATALOG_FORM_KEY)
        if not catalog_form_metadatas:
            raise CacheNotExistsError(
                "catalog from cache not exists, please re-initialize")
        return catalog_form_metadatas

    def get_format_catalog_metadata(self):
        """
        get format catalog
        :return:
        {
            "catalog":
                {
                    "catalog_form":
                        {
                            "name": "xxxx",
                            "version": "",
                            "alias": "Mysql",
                            "isGlobal": false,
                            "description": "xxx",
                            "invisible": false
                        }
                }
        }
        """
        catalog_form_metadata_cache = self.get_catalog_form_metadata_for_cache()
        catalog_form_metadata = format_catalog_form_metadata(
            catalog_form_metadata_cache,
            self.lang,
            self.invisible
        )
        return catalog_form_metadata

    def get_catalogs_forms(self):
        catalog_forms = []
        catalog_form_metadata = self.get_format_catalog_metadata()
        catalog_forms_metadta = DictUtils().get_items(
            catalog_form_metadata, self.catalog)
        if not catalog_forms_metadta:
            return catalog_forms
        for catalog_form_info in catalog_forms_metadta.values():
            catalog_forms.append(catalog_form_info)
        return catalog_forms

    def get_catalogs_form(self):
        catalog_form = {}
        catalog_form_metadata = self.get_format_catalog_metadata()
        catalog_forms_metadta = DictUtils().get_items(
            catalog_form_metadata, self.catalog)
        if not catalog_forms_metadta:
            return catalog_form

        catalog_form = DictUtils().get_items(
            catalog_forms_metadta, [self.app_form])
        if not catalog_form:
            raise CatalogFormMatchError(
                f"{self.catalog} not found {self.app_form}")

        return catalog_form

    def get_catalog_form_data(self):
        catalog_form_data = cache_instance.get(
            CATALOG_FROM_DATA_KEY.format(self.catalog, self.app_form)
        )
        if not catalog_form_data:
            return {}
        return catalog_form_data

    def get_catalog_forms_install(self, org=None, bdc=None):
        params = None
        if bdc:
            params = {
                "bdcName": bdc
            }
        form_application_install = {}
        all_application_data = OamApplication().list_all(params)
        # deal with get application data is empty list or None
        if all_application_data:
            for application_data in all_application_data:
                if not application_data:
                    continue
                application_format_obj = (
                    FormatCatalogRuntimeApplication(application_data))

                application_org = application_format_obj.get_bdc_org()
                application_bdc = application_format_obj.get_bdc_name()
                application_form = application_format_obj.get_app_form()
                if self.app_form != application_form:
                    continue
                if org and org != application_org:
                    continue

                if application_org not in form_application_install:
                    form_application_install[application_org] = [application_bdc]
                    continue
                if application_bdc not in form_application_install[application_org]:
                    form_application_install[application_org].append(application_bdc)

        install_data = []
        if form_application_install:
            for org, bdc in form_application_install.items():
                install_data.append({
                    "org": org,
                    "bdc": bdc
                })

        catalog_forms_install = {
            "name": self.app_form,
            "installtion": install_data
        }
        return catalog_forms_install

    def get_catalog_form_readme(self):
        if self.catalog is None or self.app_form is None:
            raise APIRequestedInvalidParamsError("catalog or app form is None")
        catalog_file = os.path.join(
            CATALOG_FROM_README_DIR,
            self.app_form,
            I18N,
            self.lang,
            README_HTML
        )
        return FileUtils().read_file(catalog_file)

    def get_form_info(self):
        """
        get form info
        :return: {"form_name": "catalog_name"}
        """
        form_info = {}
        catalog_form_metadata = self.get_format_catalog_metadata()
        for catalog, catalog_forms in catalog_form_metadata.items():
            for catalog_form in catalog_forms.keys():
                form_info[catalog_form] = catalog
        return form_info
