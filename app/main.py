from app.config.settings import DATA_DIR, make_filename
from app.services.orders_service import OrdersService
from app.storage.csv_storage import CSVStorage


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


if __name__ == "__main__":
    main()
