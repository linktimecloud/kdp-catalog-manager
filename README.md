[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
![Tests](https://github.com/linktimecloud/kdp-catalog-manager/actions/workflows/unit-test.yml/badge.svg)
![Build](https://github.com/linktimecloud/kdp-catalog-manager/actions/workflows/ci-build.yml/badge.svg)
![](https://img.shields.io/badge/python-3.10.13-green)
![](https://img.shields.io/badge/fastapi-0.110.0-green)
![image version](https://img.shields.io/docker/v/linktimecloud/kdp-catalog-manager)
![image size](https://img.shields.io/docker/image-size/linktimecloud/kdp-catalog-manager)


# KDP Catalog Manager

English | [简体中文](./README_zh.md)
<br>

## Project Description

### Project Overview
KDP Catalog Manager is a big data application management platform. It categorizes and manages applications based on their functionalities, reducing the complexity of application management and allowing big data administrators to focus more on data processing.

### Core Technical Architecture
![kdp-catalog-manager](kdp-catalog-manager.png)



### Functional Module Description

#### api
* view  
Defines Restful APIs and performs basic validation on user input parameters and output results.

#### Domain

* service  
Business logic.

* format  
Data conversion layer, used for transforming data between cached data and business data.

* model  
Data model entities.



##### Modules
* cache  
Data storage layer, where static data is stored in the cache.

* requests  
External data invocation, used to call external services to retrieve data.


## Directory Structure
```shell
├── CODEOWNERS
├── README.md
└── kdp_catalog_manager
   ├── api
   ├── common
   ├── config
   ├── main.py             # 服务启动程序
   ├── requirements.txt
   ├── test_main.py
   ├── domain
   ├── modules
   └── utils
```

## Startup Procedure

### Development Environment Setup

* Requires Python3.10+


1. Clone the code to your local machine.
```shell
git clone xxx && cd kdp-catalog-manager
```

2. Set up a virtual environment:
```shell
#Install virtualenv
pip install virtualenv
virtualenv -p /usr/local/bin/python3 venv
# Activate the virtual environment:
source ./venv/bin/activate

# Deactivate the virtual environment:
deactivate
```

3. Install dependencies:
```shell
pip install -r docker/python/requirements.txt
```

4. Start the service:
```shell
cd ~/kdp-catalog-manager \
&& export PYTHONPATH=$PYTHONPATH:$(pwd)
python kdp_catalog_manager/main.py

```

### API Manual
* After starting the service, you can view the list of available endpoints by accessing http://127.0.0.1:8888/docs.