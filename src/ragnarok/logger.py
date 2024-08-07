import logging
import sys
from typing import Optional

class RAGnarokFormatter(logging.Formatter):
    BLUE = "\033[94m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BOLD = "\033[1m"
    RESET = "\033[0m"

    def __init__(self, fmt=None, datefmt=None, style='%', validate=True):
        super().__init__(fmt, datefmt, style, validate)

    def format(self, record):
        level_color = self.BLUE
        if record.levelno == logging.WARNING:
            level_color = self.YELLOW
        elif record.levelno == logging.ERROR:
            level_color = self.RED
        elif record.levelno == logging.CRITICAL:
            level_color = self.RED + self.BOLD

        # Add RAGnarok identifier to the log message
        custom_msg = f"{self.BOLD}RAGnarok{self.RESET} | {level_color}{record.levelname}{self.RESET}: {record.msg}"
        record.msg = custom_msg
        return super().format(record)

class RAGnarokLogger:
    @staticmethod
    def setup_logging(
        level: str = "INFO",
        file_path: Optional[str] = None
    ):
        logger = logging.getLogger("ragnarok")
        logger.setLevel(level)

        # Create console handler with custom formatter
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(RAGnarokFormatter("%(asctime)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S"))
        logger.addHandler(console_handler)

        # If file path is provided, add file handler
        if file_path:
            file_handler = logging.FileHandler(file_path)
            file_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
            logger.addHandler(file_handler)

        # Set Playwright's logger to WARNING to reduce noise
        logging.getLogger('playwright').setLevel(logging.WARNING)

    @staticmethod
    def get_logger() -> logging.Logger:
        return logging.getLogger("ragnarok")