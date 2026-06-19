import os
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

WB_TOKEN = os.getenv("WB_TOKEN")

API_URL = "https://statistics-api.wildberries.ru/api/v1/supplier/orders"

DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

LOGS_DIR = Path("logs")
LOGS_DIR.mkdir(exist_ok=True)
LOGS_LEVEL = 2


def make_filename(query: str, ext: str):
    """
    Создаёт имя файла с временной меткой.
    Args:
        query (str): Базовый префикс имени файла.
        ext (str): Расширение файла (без точки).
    Returns:
        str: Сформированное имя файла в формате "{query}_{timestamp}.{ext}".
    """
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    safe_query = query.replace(" ", "_")
    return f"{safe_query}_{timestamp}.{ext}"
