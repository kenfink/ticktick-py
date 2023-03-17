from datetime import datetime, timedelta
from ticktick.helpers import time_methods


class FocusTimeManager:
    POMO_BASE_URL = 'https://api.ticktick.com/api/v2/pomodoros'

    def __init__(self, client_class):
        self._client = client_class
        self.access_token = ''

    #   ---------------------------------------------------------------------------------------------------------------
    #   Focus Timer Methods

    def focused_hour_average_statistic(self, start_date=datetime.now() - timedelta(days=30), end_date=datetime.now):
        """
        Returns:
            dict mapping time-of-day-hour to focused minutes average in the given timeframe
        """
        return self._client.http_get(
            url=self.POMO_BASE_URL + "/statistics/dist/clock/"
                + time_methods.convert_date_to_stamp(start_date)
                + "/" + time_methods.convert_date_to_stamp(end_date),
            cookies=self._client.cookies,
            headers=self._client.HEADERS)

    def focused_hour_statistic(self, start_date=datetime.now() - timedelta(days=7), end_date=datetime.now()):
        """
        Returns:
            daily focus times
        Example:
              Method call for the 17th of March 2023 returns:
              [
                {
                    "timeDurations": {
                        "11": 39,
                        "13": 20,
                        "14": 39,
                        "10": 20
                    },
                    "day": "20230317",
                    "timezone": "Europe/Berlin"
                }
            ]
            Note that timeDurations maps the hour of day to focused minutes.
            Use helpers.time_methods.convert_stamp_to_date to convert the day-stamp into a daytime object
        """

        return self._client.http_get(url=self.POMO_BASE_URL + "/statistics/dist/clockByDay/"
                                         + time_methods.convert_date_to_stamp(start_date)
                                         + "/" + time_methods.convert_date_to_stamp(end_date),
                                     cookies=self._client.cookies,
                                     headers=self._client.HEADERS)

    def focused_time_statistic(self, start_date=datetime.now() - timedelta(days=1), end_date=datetime.now()):
        """
        Returns:
            Focused time in minutes categorized by project, tag and task.

        Example:
            {
                "projectDurations": {
                    "HABIT_CATEGORY": 68,
                    "UNKNOWN_CATEGORY": 520,
                },
                "tagDurations": {
                    "HABIT_CATEGORY": 68,
                    "UNKNOWN_CATEGORY": 1557,
                    "asap": 466
                },
                "taskDurations": {
                    "Work on TickTick API...": 123,
                }
            }
        """
        return self._client.http_get(url=self.POMO_BASE_URL + "/statistics/dist/"
                                         + time_methods.convert_date_to_stamp(start_date)
                                         + "/" + time_methods.convert_date_to_stamp(end_date),
                                     cookies=self._client.cookies,
                                     headers=self._client.HEADERS)
