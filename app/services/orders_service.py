import pandas as pd

from app.clients.wildberries_client import WildberriesClient
from app.config.logging import setup_logger
from app.utils.dates import get_yesterday_range


class OrdersService:
    def __init__(self):
        self.client = WildberriesClient()
        self.logger = setup_logger(name=__name__, log_to_console=True)

    def _fetch_orders(self) -> dict:
        """
        Загружает данные о заказах за вчерашний день.
        Returns:
            dict: Сырые данные о заказах.
        """
        start, _ = get_yesterday_range()

        return self.client.get_orders(date_from=start.strftime("%Y-%m-%d"))

    def _transform(self, data: dict) -> pd.DataFrame:
        """
        Преобразует сырые данные API в структурированный DataFrame.
        Извлекает и форматирует поля: дату, артикул, название товара, статус, цену.
        Args:
            data: dict - Сырые данные из API Wildberries.
        Returns:
            pd.DataFrame - Обработанные данные о заказах.
        """
        rows = []

        for item in data:
            try:
                order_date_raw = item.get("date")
                rows.append(
                    {
                        "order_date": pd.to_datetime(order_date_raw, errors="coerce").strftime("%d-%m-%Y")
                        if order_date_raw
                        else None,
                        "article": item.get("supplierArticle"),
                        "product_name": f"{item.get('brand', '')} {item.get('subject', '')}".strip(),
                        "status": "Cancelled" if item.get("isCancel") else "Active",
                        "price": float(item.get("totalPrice", 0)) if item.get("totalPrice") else 0.0,
                    }
                )
            except Exception as exc:
                self.logger.warning("Failed to process order %s: %s", item.get("srid"), exc)
                continue

        return pd.DataFrame(rows)

    @staticmethod
    def get_top_articles(df: pd.DataFrame) -> pd.DataFrame:
        """
        Находит топ‑3 самых частых артикулов в DataFrame.
        Args:
            df: pd.DataFrame - DataFrame с данными о заказах.
        Returns:
            pd.DataFrame - Топ‑3 артикулов с количеством заказов.
        """
        top = df.groupby("article").size().reset_index(name="count").sort_values("count", ascending=False).head(3)
        return top

    def run(self) -> pd.DataFrame:
        """
        Основной метод сервиса: выполняет загрузку и преобразование данных о заказах.
        Returns:
            pd.DataFrame: Готовый DataFrame с обработанными данными о заказах.
        """
        raw = self._fetch_orders()
        df = self._transform(raw)

        return df

    @staticmethod
    def build_top_articles_message(top_df: pd.DataFrame) -> str:
        lines = ["Топ-3 артикула по количеству заказов за вчера:", ""]

        for idx, row in enumerate(top_df.itertuples(), start=1):
            lines.append(f"{idx}. {row.article} — {row.count} заказов")

        return "\n".join(lines)
