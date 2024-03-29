FROM python:3.10.13-bullseye AS builder

WORKDIR /workspace

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv ${VIRTUAL_ENV}
ENV PATH="${VIRTUAL_ENV}/bin:$PATH"

# Install Python dependencies
COPY docker/python/requirements.txt .
COPY docker/bin/entrypoint.sh .
#COPY version.py .
COPY kdp_catalog_manager kdp_catalog_manager/
RUN ${VIRTUAL_ENV}/bin/pip3 install --no-cache-dir --upgrade pip setuptools Cython==3.0.8 \
    && ${VIRTUAL_ENV}/bin/pip3 install --no-cache-dir --upgrade --force-reinstall -r requirements.txt \
    && rm -f requirements.txt \
    && cd kdp_catalog_manager && python setup.py build_ext --inplace  \
    && ${VIRTUAL_ENV}/bin/python setup.py build_ext clean -a && rm -f setup.py && rm -rf build


FROM python:3.10.13-bullseye

ENV TZ=${TZ:-Asia/Shanghai}
ARG RUNTIME_HOME
ENV RUNTIME_HOME=${RUNTIME_HOME:-/opt/bdos/kdp/bdos-core}
ENV BDOS_USER=${BDOS_USER:-bdos}
ENV BDOS_USER_HOME=${BDOS_USER_HOME:-/home/${BDOS_USER}}


WORKDIR ${RUNTIME_HOME}

RUN apt-get update \
    && apt-get -y install sudo \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && cp /usr/share/zoneinfo/${TZ} /etc/localtime \
    && echo ${TZ} > /etc/timezone \
    && adduser -q --disabled-password --shell /bin/bash ${BDOS_USER}  \
    && echo "${BDOS_USER} ALL=(root) NOPASSWD:ALL" > /etc/sudoers.d/${BDOS_USER}  \
    && chmod 0440 /etc/sudoers.d/${BDOS_USER} \
    && chown -R ${BDOS_USER}:${BDOS_USER} ${BDOS_USER_HOME} \
    && mkdir ${RUNTIME_HOME}/logs \
    && chown -R ${BDOS_USER}:${BDOS_USER} ${RUNTIME_HOME}

ENV PYTHONPATH=${RUNTIME_HOME}
ENV VIRTUAL_ENV=/opt/venv
ENV PATH="${VIRTUAL_ENV}/bin:$PATH"
COPY --chown=${BDOS_USER}:${BDOS_USER} --from=builder /workspace .
COPY --chown=${BDOS_USER}:${BDOS_USER} --from=builder /opt/venv /opt/venv

USER ${BDOS_USER}
CMD ["/bin/sh", "-c", "${RUNTIME_HOME}/entrypoint.sh"]