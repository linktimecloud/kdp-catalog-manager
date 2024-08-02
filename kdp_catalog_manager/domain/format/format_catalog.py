#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from kdp_catalog_manager.domain.format.base import Format
from kdp_catalog_manager.utils.dictutils import DictUtils
from kdp_catalog_manager.config.base_config import DEFAULT_LANG
from kdp_catalog_manager.common.constants import I18N


class FormatCatalog(Format):
    def __init__(self, raw):
        super().__init__(raw)

    def get_name(self):
        return DictUtils().get_items(self.raw, ["name"])

    def get_type(self):
        return DictUtils().get_items(self.raw, ["isGlobal"], False)

    def get_category(self, lang=DEFAULT_LANG):
        if lang == DEFAULT_LANG:
            return DictUtils().get_items(self.raw, ["category"])
        return DictUtils().get_items(self.raw, [I18N, lang, "category"])

    def get_description(self, lang=DEFAULT_LANG):
        if lang == DEFAULT_LANG:
            return DictUtils().get_items(self.raw, ["description"])
        return DictUtils().get_items(self.raw, [I18N, lang, "description"])

    def get_global(self):
        return DictUtils().get_items(self.raw, ["isGlobal"], False)

    def get_image(self):
        return DictUtils().get_items(self.raw, ["image"], "")

    def get_group(self):
        return DictUtils().get_items(self.raw, ["group"], "BigDataComponent")
