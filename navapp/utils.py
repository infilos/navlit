import os
import sys
import time

import streamlit as st
from loguru import logger

# this is conflict with stylable_container
# from streamlit_javascript import st_javascript


def not_none(value: object) -> bool:
    return value is not None


def not_empty(value: str) -> bool:
    return value is not None and len(value) > 0


def is_datetime(value: str) -> bool:
    return not_empty(value) and not value.startswith("0000-00-00")


def is_int(value: str) -> bool:
    return not_empty(value) and value.isdigit()


def build_conf_dir():
    return os.path.join(os.getcwd(), 'config')


def build_log_dir():
    return os.path.join(os.getcwd(), 'logs')


@st.cache_resource
def setup_logging(env="dev", level="INFO"):
    logger.remove()
    log_format = "{time:YYYY-MM-DD HH:mm:ss} | {name} {function} {line} | {level} | {message}"
    logger.configure(extra={"ip": "", "user": ""})

    if env == "dev":
        logger.add(sys.stderr, level="DEBUG", format=log_format, colorize=True, backtrace=True, diagnose=True)
    else:
        log_dir = build_log_dir()
        logger.add(
            sink=f"{log_dir}/log_{time.strftime('%Y%m%d')}.log",
            mode='a',
            level=level,
            rotation='00:00',
            retention=3,
            format="{time:YYYY-MM-DD HH:mm:ss} | {name} {function} {line} | {level} | {message}"
        )


# noinspection PyBroadException
# def get_user_ip():
#     try:
#         url = 'https://api.ipify.org?format=json'
#         script = (f'await fetch("{url}").then('
#                   'function(response) {'
#                   'return response.json();'
#                   '})')
#         result = st_javascript(script)
#         if isinstance(result, dict) and 'ip' in result:
#             return result['ip']
#     except Exception as e:
#         pass
#     return None
