#!/usr/bin/env python
# -*- coding: utf-8 -*-

from functools import reduce


class DictUtils(object):

    @staticmethod
    def get_items(obj, items, default=None):
        """递归获取数据

        :param obj:
        :param default:
        :param items: 键列表：['foo', 'bar']，或者用 "." 连接的键路径： ".foo.bar" 或 "foo.bar"
        """
        if isinstance(items, str):
            items = items.strip(".").split(".")
        try:
            return reduce(lambda x, i: x[i], items, obj)
        except (IndexError, KeyError, TypeError):
            return default
