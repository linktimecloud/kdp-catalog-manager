#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from fastapi import APIRouter

from kdp_catalog_manager.api.api_v1.endpoints import catalog
from kdp_catalog_manager.api.api_v1.endpoints import catalog_app_form
from kdp_catalog_manager.api.api_v1.endpoints import catalog_app_runtime

api_router = APIRouter()

# 分组路由
api_router.include_router(catalog.router, tags=["Catalog"])
api_router.include_router(
    catalog_app_form.router, tags=["CatalogAppForm"]
)
api_router.include_router(
    catalog_app_runtime.router, tags=["CatalogRuntime"]
)
