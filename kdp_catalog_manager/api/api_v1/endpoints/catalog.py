#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from typing import Annotated

from fastapi import APIRouter, Path, Response, status, Header
from fastapi.responses import HTMLResponse

from kdp_catalog_manager.common.constants import CATALOG_DESC, \
    NOT_FOUND_README_HTML
from kdp_catalog_manager.config.base_config import DEFAULT_LANG, SUPPORT_LANG
from kdp_catalog_manager.domain.model.catalog import CatalogList, \
    CatalogDataOut
from kdp_catalog_manager.domain.service.catalog import CatalogController
from kdp_catalog_manager.exceptions.exception import KdpCatalogManagerError, \
    FileNotExistsError, LangNotSupport
from kdp_catalog_manager.utils.format_return import FormatReturn

router = APIRouter()


@router.get("/catalogs",
            response_model=CatalogList,
            summary="获取应用目录列表",
            description="获取应用目录列表操作")
async def read_catalogs(
        accept_language: Annotated[str, Header(description="请求语言类型")] = DEFAULT_LANG
):
    """获取catalog 列表"""
    try:
        if accept_language not in SUPPORT_LANG:
            raise LangNotSupport(
                f"Header Accept-Language is:{accept_language}, "
                f"not in {SUPPORT_LANG}")
        data = CatalogController(lang=accept_language).get_catalogs()
        rtn = FormatReturn().format_return_json(
            data, msg="get catalogs data success")
    except KdpCatalogManagerError as error:
        error_info = FormatReturn().format_error_info(
            error.error_name,
            error.error_details,
            error_msg=error.error_cname
        )
        rtn = FormatReturn().format_return_json(
            [], status=1, msg=error.error_cname, error_info=error_info)
    return rtn


@router.get("/catalogs/{catalog}",
            response_model=CatalogDataOut,
            summary="获取应用目录信息",
            description="获取某个应用目录信息操作")
async def read_catalog(
        catalog: Annotated[str, Path(description=CATALOG_DESC)],
        accept_language: Annotated[str, Header(description="请求语言类型")] = DEFAULT_LANG
):
    """获取catalog 信息"""
    try:
        if accept_language not in SUPPORT_LANG:
            raise LangNotSupport(
                f"Header Accept-Language is:{accept_language}, "
                f"not in {SUPPORT_LANG}")
        data = CatalogController(
            catalog=catalog, lang=accept_language).get_catalog()
        rtn = FormatReturn().format_return_json(
            data, msg="get catalogs data success")
    except KdpCatalogManagerError as error:
        error_info = FormatReturn().format_error_info(
            error.error_name,
            error.error_details,
            error_msg=error.error_cname
        )
        rtn = FormatReturn().format_return_json(
            {}, status=1, msg=error.error_cname, error_info=error_info)
    return rtn


@router.get("/catalogs/{catalog}/readme",
            response_class=HTMLResponse,
            summary="获取应用目录说明",
            description="获取某个应用目录说明操作")
async def read_catalog_readme(
        response: Response,
        catalog: Annotated[str, Path(description=CATALOG_DESC)],
        accept_language: Annotated[str, Header(description="请求语言类型")] = DEFAULT_LANG
):
    """获取catalog 说明"""
    try:
        if accept_language not in SUPPORT_LANG:
            raise LangNotSupport(
                f"Header Accept-Language is:{accept_language}, "
                f"not in {SUPPORT_LANG}")
        rtn = CatalogController(
            catalog, lang=accept_language).get_catalog_readme()
    except FileNotExistsError:
        response.status_code = status.HTTP_404_NOT_FOUND
        rtn = NOT_FOUND_README_HTML
    except LangNotSupport:
        response.status_code = status.HTTP_400_BAD_REQUEST
        rtn = "语言不支持:Header Accept-Language is:ens, not in ['zh', 'en']"
    return rtn
