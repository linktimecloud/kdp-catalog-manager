#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from pydantic import BaseModel, Field


class Response(BaseModel):
    status: int = Field(default=0, description="状态码， 1：失败， 0：成功")
    message: str = Field(description="描述信息")
    data: dict = Field(description="返回数据")
    error: dict = Field(description="错误信息")
