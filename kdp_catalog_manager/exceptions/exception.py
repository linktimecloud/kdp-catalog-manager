#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import traceback
import os
from kdp_catalog_manager.utils.log import logger


def get_exception():
    # 获取异常的跟踪信息
    exc_traceback = traceback.format_exc()

    # 提取文件名部分并打印跟踪信息
    basename_traceback = os.path.basename(exc_traceback)
    logger.error(basename_traceback)


class KdpCatalogManagerError(Exception):
    def __init__(self, error_cname=None):
        self.error_name = self.__class__.__name__
        self.error_details = get_exception()
        if not error_cname:
            self.error_cname = "Kdp Catalog Manager Error"
        else:
            self.error_cname = "{}".format(error_cname)
        super().__init__(self.error_cname)

    def __repr__(self):
        return "'{}({})'".format(self.error_name, self.error_cname)


class LangNotSupport(KdpCatalogManagerError):
    def __init__(self, name):
        self.error_cname = "语言不支持:{}".format(name)
        KdpCatalogManagerError.__init__(self, self.error_cname)


class DirectoryNotExistsError(KdpCatalogManagerError):
    def __init__(self, file_path):
        self.error_cname = "路径 {} 不存在".format(file_path)
        KdpCatalogManagerError.__init__(self, self.error_cname)


class FileNotExistsError(KdpCatalogManagerError):
    def __init__(self, file_path):
        self.error_cname = "文件 {} 不存在".format(file_path)
        KdpCatalogManagerError.__init__(self, self.error_cname)


class ReadFileError(KdpCatalogManagerError):
    def __init__(self, file_path):
        self.error_cname = "读取文件 {} 失败".format(file_path)
        KdpCatalogManagerError.__init__(self, self.error_cname)


class HTTPRequestError(KdpCatalogManagerError):
    def __init__(self, method, url, params=None, payload=None, msg=None):
        __basic_error_cname = "请求method={} url={}失败 {},请检查该服务是否运行正常".format(method, url, msg)
        self.error_cname = __basic_error_cname
        if params:
            self.error_cname = "{}(请求参数Params={})".format(__basic_error_cname, params)
        if payload:
            self.error_cname = "{}(请求参数Body={})".format(__basic_error_cname, payload)
        if params and payload:
            self.error_cname = "{}(请求参数Params={},Body={})".format(__basic_error_cname, params, payload)
        KdpCatalogManagerError.__init__(self, self.error_cname)


class APIRequestedURLNotFoundError(KdpCatalogManagerError):
    def __init__(self):
        self.error_cname = "API 请求URL不存在"
        KdpCatalogManagerError.__init__(self, self.error_cname)


class APIRequestedInvalidParamsError(KdpCatalogManagerError):
    def __init__(self, error_msg=""):
        self.error_cname = "API 请求参数不正确:{}".format(error_msg)
        KdpCatalogManagerError.__init__(self, self.error_cname)


class WriteFileError(KdpCatalogManagerError):
    def __init__(self, file_path):
        self.error_cname = "保存(写)文件 {} 失败".format(file_path)
        KdpCatalogManagerError.__init__(self, self.error_cname)


class FileOpsForbidden(KdpCatalogManagerError):
    def __init__(self, file_path):
        self.error_cname = "文件路径 {} 不合法".format(file_path)
        KdpCatalogManagerError.__init__(self, self.error_cname)


class CreateSoftLinkError(KdpCatalogManagerError):
    def __init__(self, src, dst):
        self.error_cname = "创建软链 {}->{} 失败".format(src, dst)
        KdpCatalogManagerError.__init__(self, self.error_cname)


class MaxTryError(KdpCatalogManagerError):
    """超过最大重试次数"""


class LoadYamlError(KdpCatalogManagerError):
    def __init__(self, name=""):
        self.error_cname = "获取YAML失败:{}".format(name)
        KdpCatalogManagerError.__init__(self, self.error_cname)


class CopyFileError(KdpCatalogManagerError):
    def __init__(self, error_msg):
        self.error_cname = "拷贝文件失败 {}".format(error_msg)
        KdpCatalogManagerError.__init__(self, self.error_cname)


class DirNotExistsError(KdpCatalogManagerError):
    def __init__(self, dir_path):
        self.error_cname = "目录 {} 不存在".format(dir_path)
        KdpCatalogManagerError.__init__(self, self.error_cname)


class CopyDirError(KdpCatalogManagerError):
    def __init__(self, error_msg):
        self.error_cname = "拷贝目录失败 {}".format(error_msg)
        KdpCatalogManagerError.__init__(self, self.error_cname)


class RemoveDirError(KdpCatalogManagerError):
    def __init__(self, error_msg):
        self.error_cname = "删除目录失败 {}".format(error_msg)
        KdpCatalogManagerError.__init__(self, self.error_cname)


class GetAppInfoError(KdpCatalogManagerError):
    def __init__(self, error_msg=""):
        self.error_cname = "获取应用描述信息失败 {}".format(error_msg)
        KdpCatalogManagerError.__init__(self, self.error_cname)


class ConvertEngineDataError(KdpCatalogManagerError):
    def __init__(self, name=""):
        self.error_cname = "[实例化应用]转换配置失败 {}".format(name)
        KdpCatalogManagerError.__init__(self, self.error_cname)


class JSONSchemaError(KdpCatalogManagerError):
    def __init__(self, name=""):
        self.error_cname = "JSONSchemaError:{}".format(name)
        KdpCatalogManagerError.__init__(self, self.error_cname)


class CacheNotSupportError(KdpCatalogManagerError):
    def __init__(self, name=""):
        self.error_cname = f"缓存类型{name}不支持"
        KdpCatalogManagerError.__init__(self, self.error_cname)


class CacheOperatorError(KdpCatalogManagerError):
    def __init__(self, name=""):
        self.error_cname = f"缓存操作失败: {name}"
        KdpCatalogManagerError.__init__(self, self.error_cname)


class CacheNotExistsError(KdpCatalogManagerError):
    def __init__(self, name=""):
        self.error_cname = f"缓存不存在: {name}"
        KdpCatalogManagerError.__init__(self, self.error_cname)


class LoadJSONFileError(KdpCatalogManagerError):
    def __init__(self, file_path):
        self.error_cname = f"读取的{file_path} 配置文件内容不是合法的JSON格式"
        KdpCatalogManagerError.__init__(self, self.error_cname)


class DataNoneError(KdpCatalogManagerError):
    def __init__(self, file_path):
        self.error_cname = f"内容为空:{file_path}"
        KdpCatalogManagerError.__init__(self, self.error_cname)


class CatalogFormMatchError(KdpCatalogManagerError):
    def __init__(self, error_msg):
        self.error_cname = f"应用目录与应用模板不匹配: {error_msg}"
        KdpCatalogManagerError.__init__(self, self.error_cname)


class DataTypeError(KdpCatalogManagerError):
    def __init__(self, error_msg):
        self.error_cname = f"数据类型异常: {error_msg}"
        KdpCatalogManagerError.__init__(self, self.error_cname)


class GetDataError(KdpCatalogManagerError):
    def __init__(self, error_msg):
        self.error_cname = f"获取数据类型: {error_msg}"
        KdpCatalogManagerError.__init__(self, self.error_cname)