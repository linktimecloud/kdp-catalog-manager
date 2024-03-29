#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from fastapi import APIRouter, Query
from typing import Annotated

from kdp_catalog_manager.common.constants import (CATALOG_DESC,
                                                  FORM_DESC, BDC_DESC)
from kdp_catalog_manager.domain.model.catalog_app_runtime import CatalogAppList
from kdp_catalog_manager.domain.service.application import ApplicationController
from kdp_catalog_manager.utils.format_return import FormatReturn
from kdp_catalog_manager.exceptions.exception import KdpCatalogManagerError


router = APIRouter()


@router.get("/catalogs/app_forms/apps",
            response_model=CatalogAppList,
            summary="获取应用列表信息",
            description="获取应用列表信息操作")
async def read_catalog_runtimes(
        catalog: Annotated[str, Query(description=CATALOG_DESC)] = None,
        form: Annotated[str, Query(description=FORM_DESC)] = None,
        bdc: Annotated[str, Query(description=BDC_DESC)] = None,
        labelSelector: Annotated[
            str, Query(
                description="A selector to restrict the list of "
                            "returned objects by their labels. "
                            "Defaults to everything."
            )
        ] = None,
):
    """获取catalog 运行态应用列表"""
    try:
        data = ApplicationController(
            bdc=bdc, catalog=catalog, app_form=form
        ).get_applications(labelSelector)
        rtn = FormatReturn().format_return_json(
            data, msg="get catalog form data success")
    except KdpCatalogManagerError as error:
        error_info = FormatReturn().format_error_info(
            error.error_name,
            error.error_details,
            error_msg=error.error_cname
        )
        rtn = FormatReturn().format_return_json(
            [], status=1, msg=error.error_cname, error_info=error_info)
    return rtn
