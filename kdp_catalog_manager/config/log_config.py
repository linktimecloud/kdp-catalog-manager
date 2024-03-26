#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import os


LOG_DIR = os.environ.get("LOG_DIR", "logs")
LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
LOG_FILE = os.environ.get("LOG_FILE", "kdp-catalog-manager.log")
LOG_FILE_MAX_BYTES = os.environ.get('LOG_FILE_MAX_BYTES', 1024 * 1024 * 5)
LOG_FILE_BACKUP_COUNT = os.environ.get('LOG_FILE_BACKUP_COUNT', 3)


LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": "[%(asctime)s] [%(levelname)s]: %(message)s",
            "use_colors": None
        },
        "access": {
            "()": "uvicorn.logging.AccessFormatter",
            "fmt": "[%(asctime)s] [%(levelname)s] [PID:%(process)d][ThreadID:%(thread)d-%(threadName)s] - [%(status_code)s]: %(message)s"
        }
    },
    "handlers": {
        "default": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr"
        },
         "access": {
            "formatter": "access",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr"
        }
    },
    "loggers": {
        "uvicorn": {
            "handlers": ["default"],
            "level": "ERROR",
            "propagate": False
        },
        "uvicorn.error": {
            "level": "INFO"
        },
        "uvicorn.access": {
            "handlers": ["access"],
            "level": "INFO",
            "propagate": False
        }
    }
}