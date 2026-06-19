import requests

from app.config.logging import setup_logger
from app.config.settings import API_URL, WB_TOKEN


class WildberriesClient:
    """Клиент для взаимодействия с API Wildberries."""

    def __init__(self):
        self.token = WB_TOKEN
        self.logger = setup_logger(name=__name__, log_to_console=True)

    def get_orders(self, date_from: str) -> dict:
        """
        Получает данные о заказах из API Wildberries за указанный период.
        Args:
            date_from (str): Дата начала периода в формате YYYY‑MM‑DD.
        Returns:
            dict: JSON‑ответ API с данными о заказах.
        Raises:
            Exception: Если запрос к API завершился ошибкой (статус не равен 200).
        """
        headers = {"Authorization": self.token}

        params = {
            "dateFrom": date_from,
            "flag": 1,
        }

        response = requests.get(API_URL, headers=headers, params=params)

        if response.status_code != 200:
            self.logger.error("WB API error: %s", response.text)
            raise Exception(f"WB API error: {response.text}")

        return response.json()
