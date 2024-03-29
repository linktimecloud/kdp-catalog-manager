#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import os

import markdown

from kdp_catalog_manager.config.base_config import EXTEND_EXTENSION
from kdp_catalog_manager.utils.fileutils import FileUtils

MD_HTML_CSS = "kdp_catalog_manager/utils/markdown_to_html/md_html.css"


class HtmlController(object):
    def __init__(self, css_file=MD_HTML_CSS):
        self.css_file = css_file
        self.html_css = os.path.join(os.getcwd(), self.css_file)

    def get_css(self):
        return FileUtils().read_file(self.html_css)

    def create(self, data, file_name: str):
        css_data = self.get_css()
        html_data = css_data + data
        FileUtils().write_file(html_data, file_name)


class MarkdownToHtlm(HtmlController):
    def __init__(self):
        super().__init__()
        self.extensions = [
            'extra',
            'tables',
            'codehilite'
        ]
        self.extend_extensions()

    def extend_extensions(self):
        if EXTEND_EXTENSION:
            custom_extensions = EXTEND_EXTENSION.split(",")
            self.extensions.extend(custom_extensions)

    def mutate_markdown_data(self, input_file):
        try:
            markdown_data = FileUtils().read_file(input_file)
            html_data = markdown.markdown(
                markdown_data,
                extensions=self.extensions
            )
            return html_data
        except Exception:
            return None

    def markdown_to_html(self, input_file, output_file, output_dir=None):
        markdown_html_data = self.mutate_markdown_data(input_file)
        if output_dir is not None:
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            output_file = os.path.join(output_dir, output_file)
        self.create(markdown_html_data, output_file)
