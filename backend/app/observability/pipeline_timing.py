import logging
from contextlib import contextmanager
from logging.handlers import RotatingFileHandler
from pathlib import Path
from time import perf_counter

LOGGER_NAME = "tadashii.pipeline"
BACKEND_ROOT = Path(__file__).resolve().parents[2]
LOG_DIRECTORY = BACKEND_ROOT / "logs"
LOG_FILE = LOG_DIRECTORY / "pipeline_timings.txt"
LOG_FORMAT = "%(asctime)s %(levelname)s %(message)s"


def _configure_logger() -> logging.Logger:
    logger = logging.getLogger(LOGGER_NAME)

    if getattr(logger, "_tadashii_configured", False):
        return logger

    LOG_DIRECTORY.mkdir(parents=True, exist_ok=True)

    formatter = logging.Formatter(LOG_FORMAT)
    file_handler = RotatingFileHandler(
        LOG_FILE,
        maxBytes=5 * 1024 * 1024,
        backupCount=5,
        encoding="utf-8",
    )
    file_handler.setFormatter(formatter)

    terminal_handler = logging.StreamHandler()
    terminal_handler.setFormatter(formatter)

    logger.setLevel(logging.INFO)
    logger.addHandler(file_handler)
    logger.addHandler(terminal_handler)
    logger.propagate = False
    logger._tadashii_configured = True

    return logger


logger = _configure_logger()


def _format_details(details: dict) -> str:
    return " ".join(f"{name}={value}" for name, value in details.items())


@contextmanager
def timed_stage(request_id: str, stage_name: str):
    started_at = perf_counter()
    details = {}

    try:
        yield details
    except Exception:
        duration = perf_counter() - started_at
        logger.exception(
            "request=%s stage=%s duration_s=%.3f status=error",
            request_id,
            stage_name,
            duration,
        )
        raise
    else:
        duration = perf_counter() - started_at
        extra_details = _format_details(details)
        logger.info(
            "request=%s stage=%s duration_s=%.3f status=ok%s",
            request_id,
            stage_name,
            duration,
            f" {extra_details}" if extra_details else "",
        )
