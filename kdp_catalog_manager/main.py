#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import os
from contextlib import asynccontextmanager

import fastapi.openapi.utils as fu
from fastapi import FastAPI, status, Request, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from kdp_catalog_manager.api.api_v1.api import api_router
from kdp_catalog_manager.domain.service.markdown_transform_html import \
    catalog_readme, catalog_form_readme
from kdp_catalog_manager.domain.service.save_data_cache import \
    SaveCatalogDataCache, SaveCatalogFormDataCache
from kdp_catalog_manager.utils.format_return import FormatReturn
from kdp_catalog_manager.utils.log import log
from prometheus_fastapi_instrumentator import Instrumentator


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("prestart runing ......")
    instrumentator.expose(app)
    yield
    print("running before closing ......")


app = FastAPI(
    title="KDP Catalog Manager",
    version="1.0.0",
    description="应用目录管理",
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
    openapi_url="/api/v1/openapi.json",
    lifespan=lifespan
)

# 添加监控指标
instrumentator = Instrumentator().instrument(app)

# 添加路由前缀
app.include_router(api_router, prefix="/api/v1")


@app.get("/")
async def index():
    return {"ping": "pong"}


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    error_info = FormatReturn().format_error_info(
        "RequestValidationError",
        exc.errors(),
        error_msg=exc.errors()
    )
    rtn = FormatReturn().format_return_json(
        {}, status=1, msg=exc.errors(), error_info=error_info)
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder(
            rtn
        )
    )


@app.exception_handler(404)
def not_found_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=404,
        content=FormatReturn().format_return_json(
            data=exc.detail,
            status=1,
            msg=f"{request.query_params} {exc.detail}"
        )
    )


fu.validation_error_response_definition = {
    "title": "HTTPValidationError",
    "type": "object",
    "properties": {
        "status": {"title": "err status", "type": "int", "default": 1},
        "message": {"title": "Message", "type": "string"},
        "data": {"title": "data Message", "type": "object"},
        "error": {"title": "err Message", "type": "object"}
    }
}

if not os.environ.get("Test"):
    SaveCatalogDataCache().get_catalog_data()
    SaveCatalogFormDataCache().get_catalog_form_data()

    catalog_readme()
    log.info("initialization catalog readme transform to html successful")
    catalog_form_readme()
    log.info("initialization catalog form readme transform to html successful")


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(
        "main:app", host="0.0.0.0", port=8888,
    )
