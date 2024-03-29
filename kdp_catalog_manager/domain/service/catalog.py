#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import os.path

from kdp_catalog_manager.common.constants import CATALOG_KEY, I18N, README_HTML
from kdp_catalog_manager.config.base_config import DEFAULT_LANG, \
    CATALOG_README_DIR
from kdp_catalog_manager.domain.format.format_catalog import FormatCatalog
from kdp_catalog_manager.exceptions.exception import DataTypeError, \
    APIRequestedInvalidParamsError
from kdp_catalog_manager.modules.cache.cache import cache_instance
from kdp_catalog_manager.utils.dictutils import DictUtils
from kdp_catalog_manager.utils.fileutils import FileUtils


class CatalogController(object):
    def __init__(self, catalog=None, lang=DEFAULT_LANG):
        self.catalog = catalog
        self.lang = lang

    def get_catalogs_info(self):
        catalogs_info = {}
        catalogs_data = cache_instance.get(CATALOG_KEY)
        if not isinstance(catalogs_data, dict):
            raise DataTypeError(f"data type is {type(catalogs_data)}")
        for catalog, catalog_info in catalogs_data.items():
            if not catalog_info:
                catalogs_info[catalog] = {}
                continue
            catalog_format_obj = FormatCatalog(catalog_info)
            catalogs_info[catalog] = {
                "name": catalog_format_obj.get_name(),
                "description": catalog_format_obj.get_description(self.lang),
                "category": catalog_format_obj.get_category(self.lang)
            }
        return catalogs_info

    def get_catalogs(self):
        catalogs = []
        catalogs_info = self.get_catalogs_info()
        if not catalogs_info:
            return catalogs
        for catalog_info in catalogs_info.values():
            catalogs.append(catalog_info)
        return catalogs

    def get_catalog(self):
        catalogs_info = self.get_catalogs_info()
        catalog_data = DictUtils().get_items(catalogs_info, [self.catalog], {})
        return catalog_data

    def get_catalog_readme(self):
        if self.catalog is None:
            raise APIRequestedInvalidParamsError("catalog is None")
        catalog_file = os.path.join(
            CATALOG_README_DIR,
            self.catalog,
            I18N,
            self.lang,
            README_HTML
        )
        return FileUtils().read_file(catalog_file)
