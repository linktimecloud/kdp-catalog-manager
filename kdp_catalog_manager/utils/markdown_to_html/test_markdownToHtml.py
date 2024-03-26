#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import os.path
from unittest import TestCase

from .markdownToHtml import HtmlController, MarkdownToHtlm


class TestHtmlController(TestCase):
    def setUp(self):

        self.css_file = HtmlController().css_file
        with open(self.css_file, "r") as f:
            self.css_data = f.read()

    def test_get_css(self):
        rt = HtmlController().get_css()
        self.assertEqual(rt, self.css_data)

    def test_create(self):
        output_file = "test.html"
        HtmlController().create("test", output_file)
        if os.path.exists(output_file):
            self.assertEqual(True, True)
        os.remove("test.html")


class TestMarkdownToHtlm(TestCase):
    def setUp(self):
        self.markdown_data = "# desc"
        self.markdown_file = "test.md"
        with open(self.markdown_file, "w") as f:
            f.write(self.markdown_data)

    def test_mutate_markdown_data(self):
        rt = MarkdownToHtlm().mutate_markdown_data(self.markdown_file)
        self.assertEqual(rt, '<h1>desc</h1>')
