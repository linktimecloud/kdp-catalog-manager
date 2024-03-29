#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import os
import logging
from concurrent_log_handler import ConcurrentRotatingFileHandler
from kdp_catalog_manager.config import log_config


# 日志记录器
logger = logging.getLogger()
# 设置日志级别
logger.setLevel(log_config.LOG_LEVEL)

# 设置日志格式
formatter = logging.Formatter(
    "[%(asctime)s] [%(levelname)s] [PID:%(process)d][ThreadID:%(thread)d-%(threadName)s] %(module)s  %(funcName)s line:%(lineno)d %(message)s"
)

to_console = logging.StreamHandler()
to_console.setFormatter(formatter)


to_file = ConcurrentRotatingFileHandler(
    os.path.join(log_config.LOG_DIR, log_config.LOG_FILE),
    mode="a",
    maxBytes=log_config.LOG_FILE_MAX_BYTES,
    backupCount=log_config.LOG_FILE_BACKUP_COUNT
)
to_file.setFormatter(formatter)

# 将日志输出至屏幕
logger.addHandler(to_console)
# 将日志输出至文件
logger.addHandler(to_file)

log = logger


if not os.path.exists(log_config.LOG_DIR):
    os.makedirs(log_config.LOG_DIR)
