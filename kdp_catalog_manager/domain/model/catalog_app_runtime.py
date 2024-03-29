#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from typing import List

from pydantic import BaseModel, Field

from kdp_catalog_manager.domain.model.base import Response


class CatalogAppListDataMetadata(BaseModel):
    catalog: str = Field(description="应用目录名称")
    category: str = Field(description="应用目录分类")
    appForm: str = Field(description="应用模板名称")
    appName: str = Field(description="应用名称")
    appRuntime: str = Field(description="应用实例名称")
    org: str = Field(description="机构名称")
    bdc: str = Field(description="大数据集群名称")


class CatalogAppListData(BaseModel):
    name: str = Field(description="应用名称")
    isGlobal: bool = Field(default=False, description="是否为全局级别")
    status: str = Field(description="应用状态")
    updataTime: str = Field(description="应用更新时间")
    metadata: CatalogAppListDataMetadata


class CatalogAppList(Response):
    data: List
