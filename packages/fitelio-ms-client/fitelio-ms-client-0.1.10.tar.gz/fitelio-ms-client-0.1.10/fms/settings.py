import logging.config
import os

import structlog
from fms.utils import log_event_as_message, log_level_as_severity, log_timestamp_rfc3339
from structlog import processors
from structlog.contextvars import merge_contextvars
from structlog.stdlib import BoundLogger, LoggerFactory

MS_SERVER_URL = os.environ.get("MS_SERVER_URL", "0.0.0.0:50000")

LOGGING = {
    "version": 1,
    "disable_existing_loggers": True,
    "formatters": {
        "default": {"format": "[%(asctime)s] [%(levelname)8s]: %(message)s"},
        "simple": {"format": "%(message)s"},
    },
    "handlers": {
        "console": {"class": "logging.StreamHandler", "formatter": "default", "level": "DEBUG"},
        "simple": {"class": "logging.StreamHandler", "formatter": "simple", "level": "DEBUG"},
    },
    "loggers": {"fms_client": {"propagate": False, "handlers": ["simple"], "level": "DEBUG"}},
}
logging.config.dictConfig(LOGGING)

renderer_kv = processors.KeyValueRenderer(key_order=["timestamp", "severity", "message"], drop_missing=True)
renderer_json = processors.JSONRenderer()
logging_renderer = {"kv": renderer_kv, "json": renderer_json}.get(
    os.environ.get("LOGGING_RENDERER", "json"), renderer_json
)


structlog.configure(
    processors=[
        merge_contextvars,
        structlog.processors.StackInfoRenderer(),
        structlog.dev.set_exc_info,
        structlog.processors.format_exc_info,
        structlog.processors.TimeStamper(),
        structlog.stdlib.PositionalArgumentsFormatter(),
        log_timestamp_rfc3339,
        log_event_as_message,
        log_level_as_severity,
        logging_renderer,
    ],
    wrapper_class=BoundLogger,
    context_class=dict,
    logger_factory=LoggerFactory(),
    cache_logger_on_first_use=True,
)
