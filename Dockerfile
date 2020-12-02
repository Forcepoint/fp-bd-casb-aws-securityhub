FROM python:3.6.10-alpine3.11

WORKDIR /usr

ARG _HOME_DIR_NAME=fp-casb-exporter-aws
ENV _HOME_DIR_NAME=${_HOME_DIR_NAME}

COPY container-files container-files/

RUN apk update && apk add --no-cache bash \
    wget \
    && tar -zxvf container-files/${_HOME_DIR_NAME}-v*.tar.gz \
    && rm -f container-files/${_HOME_DIR_NAME}-v*.tar.gz \
    && pip install pipenv \
    && cd ${_HOME_DIR_NAME} \
    && pipenv install --skip-lock \
    && pipenv run pip freeze > requirements.txt \
    && pipenv --rm \
    && pip uninstall -y pipenv \
    && pip install --no-cache-dir -r requirements.txt \
    && cd .. \
    && chmod 755 ${_HOME_DIR_NAME}/src/modules/main_siem_watcher_stream.py \
    ${_HOME_DIR_NAME}/src/modules/main_siem_watcher_batch.py \
    container-files/entrypoint.sh

ENTRYPOINT ["./container-files/entrypoint.sh"]
