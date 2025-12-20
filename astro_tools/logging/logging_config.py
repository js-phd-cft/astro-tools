# logging_config.py - rozszerzona wersja
import sys
import logging
from logging_loki import LokiHandler

def get_logger(name: str, level: str = "INFO", loki_url: str = None):
    logger = logging.getLogger(name)
    logger.setLevel(level)
           
    if not logger.handlers:
        # Console
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(logging.Formatter(
            '%(asctime)s | %(levelname)-8s | %(name)s | %(message)s'
        ))
        logger.addHandler(handler)
        
        # Loki (opcjonalnie)
        if loki_url:
            loki = LokiHandler(
                url=f"{loki_url}/loki/api/v1/push",
                tags={"app": "teglie-pipelines", "component": name.split('.')[-1]},
                version="1"
            )
            logger.addHandler(loki)
    
    return logger

# Użycie
# logger = get_logger('gravlens.worker', loki_url='http://localhost:3100')