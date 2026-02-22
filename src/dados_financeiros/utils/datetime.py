from datetime import datetime


class DatetimeUtils:
    @staticmethod
    def hoje() -> str:
        return datetime.now().strftime("%Y-%m-%d")

    @staticmethod
    def hoje_datetime() -> datetime:
        return datetime.now()
