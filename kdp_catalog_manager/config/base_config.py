#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import os


CACHE_EXPIRE = 60*60*24*365*10


CATALOG_DIR = "catalog"
APPS_DIR = "apps"

CATALOG_README_DIR = "readme/catalog"
CATALOG_FROM_README_DIR = "readme/form"


DEFAULT_LANG = "zh"
SUPPORT_LANG = (os.environ.get("SUPPORT_LANG") or "zh,en").split(",")

# httpx connect other server setting
HTTP_TIME_OUT = int(os.environ.get("HTTP_TIME_OUT") or 10)
HTTP_MAX_RETRIES = int(os.environ.get("HTTP_MAX_RETRIES") or 3)
HTTP = "http"


# OAM config
OAM_BASE_URL = os.environ.get(
    "OAM_BASE_URL",
    default=f"{HTTP}://kdp-oam-apiserver:8000"
)


# markdown to html
EXTEND_EXTENSION = os.environ.get("EXTENSION", default=None)


# worker
WORKER_NUM = int(os.environ.get("WORKER_NUM") or 4)
LIMIT_MAX_REQUESTS = os.environ.get("LIMIT_MAX_REQUESTS", None)
TIMEOUT_KEEP_ALIVE = int(os.environ.get("TIMEOUT_KEEP_ALIVE") or 5)


# monitor
DASHBOARD_URL = os.environ.get("DASHBOARD_URL", default="https://grafana.com")
