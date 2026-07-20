
import logging
import sys

def get_logger(name: str = __name__, log_file: str = "etl_stocks.log") -> logging.Logger:
    """Configure and return a logger with console and file handlers."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)-8s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler(log_file, encoding="utf-8"),
        ],
    )
    return logging.getLogger(name)
