#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from typing import List, Dict

from pydantic import BaseModel, Field

from kdp_catalog_manager.domain.model.base import Response


class CatalogFormDataDashboardUrl(BaseModel):
    name: str = Field(description="面板名称")
    id: str = Field(description="面板id")
    link: str = Field(description="面板地址")


class CatalogFormData(BaseModel):
    name: str | None = Field(description="应用模板名称")
    version: str | None = Field(description="应用模板版本")
    alias: str | None = Field(description="应用模板别名")
    invisible: bool = Field(
        default=False, description="应用模板是否隐藏")
    isGlobal: bool = Field(default=False, description="是否为全局级别")
    description: str | None = Field(description="应用模板说明")
    catalog: str = Field(description="应用目录")
    dashboardUrl: List[CatalogFormDataDashboardUrl] | List


class CatalogFormList(Response):
    data: List[CatalogFormData] | List


class CatalogForm(Response):
    data: CatalogFormData | Dict


class CatalogFormInstallDataList(BaseModel):
    org: str = Field(description="机构名称")
    bdc: list = []


class CatalogFormInstallData(BaseModel):
    name: str = Field(description="form名称")
    installtion: List[CatalogFormInstallDataList]


class CatalogFormInstall(Response):
    data: CatalogFormInstallData
