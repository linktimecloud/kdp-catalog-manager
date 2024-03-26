#!/usr/bin/env python
# -*- encoding: utf-8 -*-

# 监听内网端口8000
bind = "0.0.0.0:8888"
# 工作模式协程。
worker_class = "uvicorn.workers.UvicornWorker"
# 不设置守护进程
daemon = 'false'
# 日志输出到stdout、stderr
errorlog = '-'
accesslog = '-'
# 日志格式
logconfig_dict = {
    'formatters': {
        "generic": {
            # 打日志的格式
            "format": "[%(asctime)s] [%(levelname)s] [PID:%(process)d][ThreadID:%(thread)d-%(threadName)s] %(message)s",
            "class": "logging.Formatter"
        }
    }
}