#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from unittest import TestCase
from .dictutils import DictUtils


class TestDicuUtils(TestCase):
    def setUp(self):
        self.raw = {"aa": 123, "bb": "123"}

    def test_get_items(self):
        rt = DictUtils().get_items(self.raw, ["aa"])
        self.assertEqual(rt, 123)

    def test_get_items_not_found(self):
        rt = DictUtils().get_items(self.raw, ["ab"])
        self.assertEqual(rt, None)

    def test_get_items1(self):
        rt = DictUtils().get_items(self.raw, ".aa")
        self.assertEqual(rt, 123)

    def test_get_items1_not_found(self):
        rt = DictUtils().get_items(self.raw, ".ab")
        self.assertEqual(rt, None)

    def test_get_items2(self):
        rt = DictUtils().get_items(self.raw, "aa")
        self.assertEqual(rt, 123)

    def test_get_items2_not_found(self):
        rt = DictUtils().get_items(self.raw, "ab")
        self.assertEqual(rt, None)

    def test_get_items3(self):
        rt = DictUtils().get_items(self.raw, "bb")
        self.assertEqual(rt, "123")
