from app.clients.telegram_client import TelegramClient
from app.config.logging import setup_logger
from app.config.settings import DATA_DIR, TG_CHAT_ID, make_filename
from app.services.orders_service import OrdersService
from app.storage.csv_storage import CSVStorage

logger = setup_logger(name=__name__, log_to_console=True)


def main():
    """
    Основная функция скрипта: получает заказы из Wildberries, преобразует их и сохраняет в CSV‑файл.
    Создаёт сервис заказов и хранилище, запускает обработку и сохраняет результат.
    """
    service = OrdersService()
    storage = CSVStorage(DATA_DIR)

    df = service.run()

    filename = make_filename("wb_orders", "csv")
    storage.save(df, filename)

    top_articles = service.get_top_articles(df)
    message = service.build_top_articles_message(top_articles)
    telegram_client = TelegramClient()
    telegram_client.send_message(chat_id=TG_CHAT_ID, text=message)
    logger.info("Telegram notification sent successfully")


if __name__ == "__main__":
    main()
