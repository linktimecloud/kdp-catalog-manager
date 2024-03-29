#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from typing import Annotated

from fastapi import APIRouter, Path, Query, Header, status, Response
from fastapi.responses import HTMLResponse

from kdp_catalog_manager.common.constants import CATALOG_DESC, FORM_DESC, \
    ORG_DESC, BDC_DESC, NOT_FOUND_README_HTML
from kdp_catalog_manager.config.base_config import DEFAULT_LANG, SUPPORT_LANG
from kdp_catalog_manager.domain.model.catalog_app_form import CatalogFormList, \
    CatalogForm, CatalogFormInstall
from kdp_catalog_manager.domain.model.catalog_app_form import \
    Response as CatalogFormData
from kdp_catalog_manager.domain.service.catalog_form import \
    CatalogFormController
from kdp_catalog_manager.exceptions.exception import LangNotSupport, \
    FileNotExistsError, KdpCatalogManagerError
from kdp_catalog_manager.utils.format_return import FormatReturn

router = APIRouter()


#
@router.get("/catalogs/{catalog}/app_forms",
            response_model=CatalogFormList,
            summary="获取应用模板列表",
            description="获取应用模板列表操作")
async def read_catalog_forms(
    catalog: Annotated[str, Path(description=CATALOG_DESC)],
    accept_language:
    Annotated[str, Header(description="请求语言类型")] = DEFAULT_LANG
):
    """获取catalog 应用模板列表"""
    try:
        if accept_language not in SUPPORT_LANG:
            raise LangNotSupport(
                f"Header Accept-Language is:{accept_language}, "
                f"not in {SUPPORT_LANG}")
        data = CatalogFormController(
            catalog=catalog, lang=accept_language
        ).get_catalogs_forms()
        rtn = FormatReturn().format_return_json(
            data, msg="get catalog form templates success")
    except KdpCatalogManagerError as error:
        error_info = FormatReturn().format_error_info(
            error.error_name,
            error.error_details,
            error_msg=error.error_cname
        )
        rtn = FormatReturn().format_return_json(
            [], status=1, msg=error.error_cname, error_info=error_info)
    return rtn


@router.get("/catalogs/{catalog}/app_forms/{form}",
            response_model=CatalogForm,
            summary="获取应用模板信息",
            description="获取某个应用模板信息操作")
async def read_catalog_form(
        catalog: Annotated[str, Path(description=CATALOG_DESC)],
        form: Annotated[str, Path(description=FORM_DESC)],
        accept_language:
        Annotated[str, Header(description="请求语言类型")] = DEFAULT_LANG
):
    """获取catalog 应用模板信息"""
    try:
        if accept_language not in SUPPORT_LANG:
            raise LangNotSupport(
                f"Header Accept-Language is:{accept_language}, "
                f"not in {SUPPORT_LANG}")
        data = CatalogFormController(
            catalog=catalog, app_form=form, lang=accept_language
        ).get_catalogs_form()
        rtn = FormatReturn().format_return_json(
            data, msg="get catalog form template success")
    except KdpCatalogManagerError as error:
        error_info = FormatReturn().format_error_info(
            error.error_name,
            error.error_details,
            error_msg=error.error_cname
        )
        rtn = FormatReturn().format_return_json(
            {}, status=1, msg=error.error_cname, error_info=error_info)
    return rtn


@router.get("/catalogs/{catalog}/app_forms/{form}/data",
            response_model=CatalogFormData,
            summary="获取应用模板信息",
            description="获取某个应用模板信息操作")
async def read_catalog_form_data(
        catalog: Annotated[str, Path(description=CATALOG_DESC)],
        form: Annotated[str, Path(description=FORM_DESC)],
):
    """获取catalog 应用模板数据"""
    try:
        data = CatalogFormController(
            catalog=catalog, app_form=form
        ).get_catalog_form_data()
        rtn = FormatReturn().format_return_json(
            data, msg="get catalog form data success")
    except KdpCatalogManagerError as error:
        error_info = FormatReturn().format_error_info(
            error.error_name,
            error.error_details,
            error_msg=error.error_cname
        )
        rtn = FormatReturn().format_return_json(
            {}, status=1, msg=error.error_cname, error_info=error_info)
    return rtn


@router.get("/catalogs/{catalog}/app_forms/{form}/install",
            response_model=CatalogFormInstall,
            summary="获取应用模板应用安装信息",
            description="获取某个应用模板应用安装信息操作")
async def read_catalog_form_install(
        catalog: Annotated[str, Path(description=CATALOG_DESC)],
        form: Annotated[str, Path(description=FORM_DESC)],
        org: Annotated[str, Query(description=ORG_DESC)] = None,
        bdc: Annotated[str, Query(description=BDC_DESC)] = None
):
    """获取catalog 应用模板安装情况"""
    try:
        data = CatalogFormController(
            catalog=catalog, app_form=form
        ).get_catalog_forms_install(org, bdc)
        rtn = FormatReturn().format_return_json(
            data, msg="get catalog form install data success")
    except KdpCatalogManagerError as error:
        error_info = FormatReturn().format_error_info(
            error.error_name,
            error.error_details,
            error_msg=error.error_cname
        )
        rtn = FormatReturn().format_return_json(
            [], status=1, msg=error.error_cname, error_info=error_info)
    return rtn


@router.get("/catalogs/{catalog}/app_forms/{form}/readme",
            response_class=HTMLResponse,
            summary="获取应用模板使用说明信息",
            description="获取某个应用模板使用说明信息操作")
async def read_catalog_form_readme(
        response: Response,
        catalog: Annotated[str, Path(description=CATALOG_DESC)],
        form: Annotated[str, Path(description=FORM_DESC)],
        accept_language:
        Annotated[str, Header(description="请求语言类型")] = DEFAULT_LANG
):
    """获取应用说明文档"""
    try:
        if accept_language not in SUPPORT_LANG:
            raise LangNotSupport(
                f"Header Accept-Language is:{accept_language}, "
                f"not in {SUPPORT_LANG}")
        rtn = CatalogFormController(
            catalog, form, lang=accept_language).get_catalog_form_readme()
    except FileNotExistsError:
        response.status_code = status.HTTP_404_NOT_FOUND
        rtn = NOT_FOUND_README_HTML
    except LangNotSupport:
        response.status_code = status.HTTP_400_BAD_REQUEST
        rtn = "语言不支持:Header Accept-Language is:ens, not in ['zh', 'en']"
    return rtn
