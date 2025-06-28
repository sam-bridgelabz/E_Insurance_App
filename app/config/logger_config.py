import json
import os

from loguru import logger


class Logger:
    @staticmethod
    def initialize_from_json(config_path="logger_format.json"):
        logger.remove()

        def db_filter(record):
            return record.get("extra", {}).get("config", False)

        def func_filter(record):
            return record.get("extra", {}).get("func", False)

        abs_path = os.path.join(os.path.dirname(__file__), config_path)
        with open(abs_path, "r") as f:
            config_log = json.load(f)

        for handler in config_log["handler"]:
            log_file_path = handler["sink"]

            log_dir = os.path.dirname(log_file_path)
            os.makedirs(log_dir, exist_ok=True)

            if not os.path.exists(log_file_path):
                with open(log_file_path, "w") as log_file:
                    log_file.write(
                        "LEVEL  | TIME                | MODULE              | LINE | MESSAGE\n"
                    )

            filter_name = handler.pop("filter", None)
            filter_func = {"config": db_filter, "func": func_filter}.get(filter_name)

            logger.add(**handler, filter=filter_func)

        logger.info("Logger initialized from JSON config.")
        return logger


logger_config = Logger.initialize_from_json()
config_logger = logger_config.bind(config=True)
func_logger = logger_config.bind(func=True)
