#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from typing import List, Dict

from pydantic import BaseModel, Field

from kdp_catalog_manager.domain.model.base import Response


class CatalogData(BaseModel):
    name: str = Field(description="应用目录")
    description: str = Field(description="应用目录说明")
    category: str = Field(description="应用目录分类")


class CatalogDataOut(Response):
    data: CatalogData | Dict


class CatalogList(Response):
    data: List[CatalogData] | List


class CatalogCategory(Response):
    data: List


class Catalogglobal(Response):
    data: List
