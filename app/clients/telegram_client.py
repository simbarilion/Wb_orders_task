import requests

from app.config.settings import TG_TOKEN


class TelegramClient:
    """Клиент для отправки сообщений через Telegram Bot API."""

    def __init__(self):
        self.base_url = f"https://api.telegram.org/bot{TG_TOKEN}"

    def send_message(self, chat_id: str, text: str) -> None:
        """
        Отправляет текстовое сообщение в указанный чат Telegram:
        - Отправляет POST‑запрос к методу sendMessage Telegram Bot API с указанными параметрами.
        - При ошибке HTTP‑запроса выбрасывает исключение.
        Args:
            chat_id (str): Идентификатор чата/пользователя, куда отправляется сообщение.
            text (str): Текст отправляемого сообщения.
        Raises:
            requests.HTTPError: Если запрос к Telegram API завершился с ошибкой.
        """
        response = requests.post(
            f"{self.base_url}/sendMessage",
            json={
                "chat_id": chat_id,
                "text": text,
            },
            timeout=10,
        )

        response.raise_for_status()
