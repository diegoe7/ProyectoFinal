import logging
from pathlib import Path

archivo = Path(__file__).parent / "datos_juego" / "errores.log"

def get_logger(nombre: str) -> logging.Logger:
    archivo.parent.mkdir(parents=True, exist_ok=True)
    logger = logging.getLogger(nombre)
    if not logger.handlers:
        handler = logging.FileHandler(archivo, encoding="utf-8")
        formatter = logging.Formatter(fmt="%(asctime)s | %(levelname)s | %(name)s | %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
    return logger
