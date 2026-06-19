from datetime import datetime, timedelta


def get_yesterday_range():
    """
    Возвращает временной диапазон за вчерашний день (начало и конец суток).
    Returns:
        tuple[datetime, datetime]: Кортеж (начало_вчера, конец_вчера).
    """
    yesterday = datetime.now() - timedelta(days=1)
    start = yesterday.replace(hour=0, minute=0, second=0, microsecond=0)
    end = yesterday.replace(hour=23, minute=59, second=59, microsecond=0)
    return start, end
