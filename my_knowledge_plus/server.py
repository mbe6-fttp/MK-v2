from pathlib import Path
import logging
import time
from logging.handlers import RotatingFileHandler

from waitress import serve

from app import app


BASE_DIR = Path(__file__).resolve().parent
LOG_FILE = BASE_DIR / "server.log"
HOST = "127.0.0.1"
PORT = 5001


logger = logging.getLogger("my_knowledge_server")
logger.setLevel(logging.INFO)

handler = RotatingFileHandler(
    LOG_FILE,
    maxBytes=2 * 1024 * 1024,
    backupCount=3,
    encoding="utf-8"
)

formatter = logging.Formatter(
    "%(asctime)s | %(levelname)s | %(message)s"
)

handler.setFormatter(formatter)

logger.addHandler(handler)


while True:

    try:

        logger.info(
            "Starting My Knowledge Plus server on %s:%s",
            HOST,
            PORT
        )

        serve(
            app,
            host=HOST,
            port=PORT,
            threads=8
        )

        logger.warning(
            "Waitress stopped unexpectedly. Restarting in 5 seconds."
        )

    except Exception:
        logger.exception(
            "SERVER CRASHED. Restarting in 5 seconds."
        )

    time.sleep(5)