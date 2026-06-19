import requests

from app.config.settings import TG_TOKEN


class TelegramClient:
    def __init__(self):
        self.base_url = f"https://api.telegram.org/bot{TG_TOKEN}"

    def send_message(self, chat_id: str, text: str) -> None:
        response = requests.post(
            f"{self.base_url}/sendMessage",
            json={
                "chat_id": chat_id,
                "text": text,
            },
            timeout=10,
        )

        response.raise_for_status()
