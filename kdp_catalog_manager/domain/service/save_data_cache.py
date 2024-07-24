#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import os

from kdp_catalog_manager.common.constants import METADATA_YAML, CATALOG_KEY, \
    CATALOG_FORM_KEY, APP_YAML, CATALOG_FROM_DATA_KEY
from kdp_catalog_manager.config.base_config import CACHE_EXPIRE
from kdp_catalog_manager.config.base_config import CATALOG_DIR, APPS_DIR
from kdp_catalog_manager.exceptions.exception import CacheOperatorError
from kdp_catalog_manager.modules.cache.cache import cache_instance
from kdp_catalog_manager.utils.log import log
from kdp_catalog_manager.utils.yamlutils import YAMLUtils
from kdp_catalog_manager.utils.fileutils import FileUtils


class SaveDataToCache(object):
    def __init__(self):
        self.cache = cache_instance


class SaveCatalogDataCache(SaveDataToCache):
    def __init__(self):
        super().__init__()
        self.catalog_dir = CATALOG_DIR

    def get_catalog_data(self):
        catalog_data = {}
        for catalog in os.listdir(self.catalog_dir):
            catalog_metadata_file = os.path.join(
                CATALOG_DIR, catalog, METADATA_YAML)
            if not os.path.exists(catalog_metadata_file):
                continue

            catalog_metadata = YAMLUtils().load_all_yaml(catalog_metadata_file)
            # get image base64 data to save cache
            image_file = os.path.join(CATALOG_DIR, catalog, f"{catalog}.png")
            image = FileUtils.get_file_base64(image_file)
            catalog_metadata["image"] = image
            catalog_data[catalog] = catalog_metadata
        rt = self.cache.set(CATALOG_KEY, catalog_data, CACHE_EXPIRE)
        if rt:
            log.info("initialization catalog data to cache successful")
        else:
            raise CacheOperatorError()


class SaveCatalogFormDataCache(SaveDataToCache):
    def __init__(self):
        super().__init__()
        self.catalog_dir = CATALOG_DIR
        self.apps = APPS_DIR

    def get_catalog_form_data(self):
        catalog_form = {}
        for catalog in os.listdir(self.catalog_dir):
            catalog_form_dir = os.path.join(
                self.catalog_dir, catalog, self.apps)
            catalog_form_metadata_info = {}
            for catalog_from_app in os.listdir(catalog_form_dir):
                if not catalog_from_app.endswith(".app"):
                    continue

                # 存储元数据至缓存中
                catalog_form_metadata_file = os.path.join(
                    catalog_form_dir, catalog_from_app, METADATA_YAML)
                if not os.path.exists(catalog_form_metadata_file):
                    continue

                catalog_form_metadata = YAMLUtils().load_all_yaml(
                    catalog_form_metadata_file)

                catalog_form_app_name = catalog_from_app.split(".")[0]
                catalog_form_metadata_info[catalog_form_app_name] = (
                    catalog_form_metadata)

                # 存储应用模板信息至缓存中
                catalog_form_data_file = os.path.join(
                    catalog_form_dir, catalog_from_app, APP_YAML
                )
                if not os.path.exists(catalog_form_data_file):
                    continue
                catalog_form_data = YAMLUtils().load_all_yaml(
                    catalog_form_data_file)

                self.cache.set(
                    CATALOG_FROM_DATA_KEY.format(catalog, catalog_form_app_name),
                    catalog_form_data,
                    CACHE_EXPIRE
                )

            catalog_form[catalog] = catalog_form_metadata_info
        rt = self.cache.set(CATALOG_FORM_KEY, catalog_form, CACHE_EXPIRE)
        if rt:
            log.info("initialization catalog from data to cache successful")
        else:
            raise CacheOperatorError("save catalog form data to cache failed")
