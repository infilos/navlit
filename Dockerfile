#FROM weastur/poetry:1.6.1-python-3.12-alpine3.17
#FROM python:3.12-alpine
FROM python:3.12-slim-bullseye

ENV PYTHONUNBUFFERED=1
ENV PYTHONIOENCODING=UTF-8

WORKDIR  /navlit
COPY . .
RUN chmod +x /navlit/logs
RUN chmod +x /navlit/config
RUN pwd
RUN ls -hl

RUN python3 -m pip --trusted-host pypi.org \
    --trusted-host pypi.python.org \
    --trusted-host=files.pythonhosted.org \
    install --upgrade pip \
    && python3 -m pip --trusted-host pypi.org \
    --trusted-host pypi.python.org \
    --trusted-host=files.pythonhosted.org \
    install --no-cache-dir --upgrade -r /navlit/requirements.txt

EXPOSE 8080
CMD streamlit run  --server.address 0.0.0.0 --server.port 8080 navapp/main.py -- --env pro
