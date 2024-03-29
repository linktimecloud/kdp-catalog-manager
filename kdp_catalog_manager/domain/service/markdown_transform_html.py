#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import os

from kdp_catalog_manager.common.constants import README, I18N
from kdp_catalog_manager.config.base_config import CATALOG_DIR, APPS_DIR, \
    CATALOG_README_DIR, CATALOG_FROM_README_DIR, DEFAULT_LANG
from kdp_catalog_manager.utils.log import log
from kdp_catalog_manager.utils.markdown_to_html.markdownToHtml import \
    MarkdownToHtlm


def deal_readme(base_dir, output_file, output_base_dir=CATALOG_README_DIR):
    for base_dir_name in os.listdir(base_dir):
        form_name = base_dir_name
        if base_dir_name.endswith(".app"):
            form_name = base_dir_name.split(".")[0]

        # 处理默认语言readme
        default_reademe_file = os.path.join(base_dir, base_dir_name, README)
        output_dir = os.path.join(
            output_base_dir, form_name, I18N, DEFAULT_LANG)
        MarkdownToHtlm().markdown_to_html(
            default_reademe_file,
            output_file,
            output_dir
        )

        # 处理其他语言readme
        readme_lang_dir = os.path.join(base_dir, base_dir_name, I18N)
        for readme_lang in os.listdir(readme_lang_dir):
            readme_lang_file = os.path.join(readme_lang_dir, readme_lang, README)
            output_dir = os.path.join(
                output_base_dir, form_name, I18N, readme_lang
            )
            MarkdownToHtlm().markdown_to_html(
                readme_lang_file,
                output_file,
                output_dir
            )


def catalog_readme():
    output_file = README.replace("md", "html")
    deal_readme(CATALOG_DIR, output_file, CATALOG_README_DIR)
    log.info("transform catalog readme to html success")


def catalog_form_readme():
    output_file = README.replace("md", "html")
    for catalog in os.listdir(CATALOG_DIR):
        catalog_form_dir = os.path.join(CATALOG_DIR, catalog, APPS_DIR)
        deal_readme(catalog_form_dir, output_file, CATALOG_FROM_README_DIR)

    log.info("transform catalog app form readme to html success")
