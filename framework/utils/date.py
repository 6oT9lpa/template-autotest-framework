from datetime import date, datetime

from framework.constants import CalendarConstants, DateFormat, DateTimeTolerance


class DateUtils:
    @staticmethod
    def today() -> date:
        return date.today()

    @staticmethod
    def current_datetime_without_seconds() -> datetime:
        return datetime.now().replace(second=0, microsecond=0)

    @staticmethod
    def format_select_date_value(value: date) -> str:
        return value.strftime(DateFormat.SELECT_DATE_VALUE)

    @staticmethod
    def parse_date_and_time_picker_value(value: str) -> datetime:
        return datetime.strptime(value, DateFormat.DATE_AND_TIME_PICKER_VALUE)

    @staticmethod
    def is_close_to_current_datetime(
        value: datetime,
        tolerance_seconds: int = DateTimeTolerance.CURRENT_DATE_TIME_SECONDS,
    ) -> bool:
        difference_seconds = abs((value - DateUtils.current_datetime_without_seconds()).total_seconds())
        return difference_seconds <= tolerance_seconds

    @staticmethod
    def nearest_future_february_29(start_date: date | None = None) -> date:
        target_date = start_date or DateUtils.today()
        year = target_date.year

        while True:
            if DateUtils.is_leap_year(year):
                leap_day = date(year, CalendarConstants.FEBRUARY, CalendarConstants.LEAP_DAY)
                if leap_day >= target_date:
                    return leap_day
            year += 1

    @staticmethod
    def is_leap_year(year: int) -> bool:
        return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)
