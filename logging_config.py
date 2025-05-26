import logging
from pathlib import Path


def setup_logger(log_name: str):
    log_dir = Path("/app/logs")
    log_dir.mkdir(parents=True, exist_ok=True)

    log_file = log_dir / f"{log_name}.log"

    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        filename=str(log_file),
        filemode="a"
    )

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
    logging.getLogger().addHandler(console_handler)
