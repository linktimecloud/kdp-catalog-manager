#!/usr/bin/env python
# -*- encoding: utf-8 -*-

CATALOG_DESC = "应用目录名称"
FORM_DESC = "应用模板名称"
ORG_DESC = "机构名称"
BDC_DESC = "大数据集群名称"
LANG_DESC = "语言类型"

METADATA_YAML = "metadata.yaml"
APP_YAML = "app.yaml"
README = "README.md"
I18N = "i18n"
README_HTML = "README.html"

# cache key
CATALOG_KEY = "catalog_info"
CATALOG_FORM_KEY = "catalog_form"
# example: catalog-form
CATALOG_FROM_DATA_KEY = "{}-{}-data"


NOT_FOUND_README_HTML = """
        <html>

        <head>
            <title>404 Not Found</title>
        </head>

        <body style="padding: 30px">
            <h1>404 Not Found</h1>
            <p>The resource could not be found.</p>
        </body>

        </html>
        """


# HTTP
HTTP_HEADER = {
    "Accept": "application/json; charset=utf-8"
}
RESPONSE_NORMAL_CODE = 200
RESPONSE_NOT_FOUND_CODE = 404
RESPONSE_DATA = "data"
