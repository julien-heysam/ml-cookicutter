import math
from datetime import date, datetime


class DateUtils:
    @staticmethod
    def readable_today_date() -> str:
        """
        Returns the current date in a readable format with day, month, and year.
        """
        return datetime.now().strftime("%d %B %Y")

    @staticmethod
    def str_to_datetime(str_date: str) -> date:
        """
        Converts a string representation of a date in the format "YYYY-MM-DD" to a `date` object.
        """
        return datetime.strptime(str_date, "%Y-%m-%d").date()

    @staticmethod
    def seconds_to_min_sec(seconds: float) -> str:
        """
        Converts a given number of seconds into minutes and seconds in the format "minutes:seconds".
        """
        minutes, sec = divmod(int(seconds), 60)
        return f"{minutes:02}:{sec:02}"

    @staticmethod
    def datetime_difference(date1: date, date2: date, how: str = "months") -> int:
        """
        Calculates the difference between two dates in either days, months, or years.
        """
        if not date1 or not date2:
            return None
        days = abs((date2 - date1).days)

        match how:
            case "days":
                return days
            case "months":
                return days // 30
            case "years":
                return days // 360
            case _:
                return days

    @staticmethod
    def months_until_date(dt: str) -> int:
        """
        Calculates the number of months until a specified date.
        """
        today = datetime.today()
        months = math.ceil((datetime.strptime(dt, "%Y-%m-%dT%H:%M:%S") - today).days / 30)
        return months

if __name__ == "__main__":
    print(DateUtils.months_until_date("2023-10-25T00:00:00"))
