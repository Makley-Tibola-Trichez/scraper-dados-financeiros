from datetime import datetime


class DatetimeUtils:

  @staticmethod
  def hoje():
    return datetime.now().strftime('%Y-%m-%d')
  
  @staticmethod
  def hoje_datetime():
    return datetime.now()