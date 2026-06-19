from pathlib import Path

from app.config.logging import setup_logger


class CSVStorage:
    """Хранилище для сохранения данных в формате CSV."""

    def __init__(self, data_dir: Path):
        self.data_dir = data_dir
        self.data_dir.mkdir(exist_ok=True)
        self.logger = setup_logger(name=__name__, log_to_console=True)

    def save(self, df, filename: str):
        """
        Сохраняет DataFrame в CSV‑файл в указанной директории.
        Если файл уже существует, логирует предупреждение и возвращает путь без сохранения.
        Args:
            df: pd.DataFrame: Данные для сохранения.
            filename: str - Имя файла для сохранения.
        Returns:
            Path: Полный путь к сохранённому файлу.
        """
        file_path = self.data_dir / filename

        if file_path.exists():
            self.logger.warning(f"File already exists: {file_path}")
            return file_path

        df.to_csv(file_path, index=False, encoding="utf-8")
        self.logger.info(f"Saved CSV: {file_path}")

        return file_path
