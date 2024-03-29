#!/bin/bash

declare RUNTIME_HOME=${RUNTIME_HOME:-"/opt/bdos/kdp/bdos-core"}
declare BDOS_USER=${BDOS_USER:-bdos}
declare CHOWN_HOST_PATH=${CHOWN_HOST_PATH:-"False"}
declare LOG_LEVEL=${LOG_LEVEL:-"info"}
declare WORKER_NUM=${WORKER_NUM:-4}
declare PARAMS_LIMIT=${PARAMS_LIMIT:-0}
declare MAX_REQUESTS=${MAX_REQUESTS:-100}
declare MAX_REQUESTS_JITTER=${MAX_REQUESTS:-100}


sudo chown ${BDOS_USER}:${BDOS_USER} ${RUNTIME_HOME} >/dev/null 2>&1

if [[ "${CHOWN_HOST_PATH}" == "True" ]];then
    echo -e "### Change owner of $RUNTIME_HOME ###"
    sudo chown -R ${BDOS_USER}:${BDOS_USER} ${RUNTIME_HOME}/kdp_catalog_manager ${RUNTIME_HOME}/logs ${RUNTIME_HOME} >/dev/null 2>&1
    echo -e "### Change owner return code: $? ###"
fi


echo -e "### Starting Server... ###"
cd ${RUNTIME_HOME}

gunicorn -c kdp_catalog_manager/config/gunicorn.py kdp_catalog_manager.main:app --workers ${WORKER_NUM} --log-level ${LOG_LEVEL} --limit-request-line=${PARAMS_LIMIT} --max-requests ${MAX_REQUESTS} --max-requests-jitter ${MAX_REQUESTS_JITTER} --preload
