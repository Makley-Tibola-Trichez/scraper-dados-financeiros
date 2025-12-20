from datetime import datetime, timezone


class DatetimeUtils:
    @staticmethod
    def hoje() -> str:
        return datetime.now(timezone.utc).strftime("%Y-%m-%d")

    @staticmethod
    def hoje_datetime() -> datetime:
        return datetime.now(timezone.utc)
