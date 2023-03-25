import secrets
from datetime import datetime


class TimerManager:
    BASE_URL = 'https://api.ticktick.com/api/v2/timer'
    POMO_BASE_URL = 'https://api.ticktick.com/api/v2/pomodoros'
    RECORD_URL = 'https://api.ticktick.com/api/v2/batch/pomodoro/timing'

    def __init__(self, client_class):
        self._client = client_class
        self.access_token = ''

    def add_timer(self, icon='habit_daily_check_in', color='#97E38B', name='Timer', timer_type='pomodoro', pomo_time=25,
                  status=0,
                  sort_order=-1099511627776, created_time=datetime.utcnow(), modified_time=datetime.utcnow()):
        """
        Adds a timer

        Arguments:
            icon: icon of the timer
            color: color of the timer
            name: name of the timer
            timer_type: pomodoro or timing
            pomo_time: pomo time in minutes. Only relevant if pomodoro type is selected
            status: status
            sort_order: sort order
            created_time: creation time
            modified_time: modification time
        """

        payload = {
            "add": [
                {"id": secrets.token_hex(12),
                 "icon": icon,
                 "color": color,
                 "name": name,
                 "type": timer_type,
                 "pomodoroTime": pomo_time,
                 "status": status,
                 "sortOrder": sort_order,
                 "createdTime": str(created_time.isoformat() + "+0000"),
                 "modifiedTime": str(modified_time.isoformat() + "+0000")}],
            "update": [],
            "delete": []
        }

        self._client.sync()
        return self._client.http_post(url=self.BASE_URL,
                                      cookies=self._client.cookies,
                                      headers=self._client.HEADERS,
                                      json=payload)

    def delete_timer(self, timer_id):
        """
        Deletes the given timer.

        Arguments:
            timer_id: The internal id of the timer
        """

        payload = {
            "add": [],
            "update": [],
            "delete": [timer_id]
        }

        self._client.sync()
        return self._client.http_post(url=self.BASE_URL,
                                      cookies=self._client.cookies,
                                      headers=self._client.HEADERS,
                                      json=payload)

    def get_all_timers(self):
        """
        Returns:
            List of timers
        """
        return self._client.http_get(url=self.BASE_URL,
                                     cookies=self._client.cookies,
                                     headers=self._client.HEADERS)

    def get_timer(self, timer_id):
        """
        Returns:
            The timer with the given id
        """
        timers = self.get_all_timers()
        for timer in timers:
            if timer['id'] == timer_id:
                return timer
        raise AttributeError("No timer with id %s found" % timer_id)

    def get_timer_id_by_name(self, name):
        """
        Returns:
            The id of the timer with the given name
        """
        timers = self.get_all_timers()
        for timer in timers:
            if timer['name'] == name:
                return timer['id']
        raise AttributeError("No timer with name " + name + " found")

    def add_record(self, tasks: list, start_time: datetime, pause_duration=0,
                   end_time: datetime = datetime.utcnow(), status=1, note=""):
        """
        Parameters:
            tasks: list of tasks. Build with build_timer_record
            start_time: start of focus time. In UTC, so adjust accordingly!
            end_time: end of focus time. In UTC, so adjust accordingly!
            pause_duration: duration of pause in seconds
            status: status
            note: focus note
        """

        payload = {
            "add": [{
                "startTime": str(start_time.isoformat() + "+0000"),
                "tasks": tasks,
                "endTime": str(end_time.isoformat() + "+0000"),
                "id": secrets.token_hex(12),
                "status": status,
                "pauseDuration": pause_duration,
                "added": "true",
                "note": note
            }],
            "update": []
        }

        return self._client.http_post(url=self.RECORD_URL,
                                      cookies=self._client.cookies,
                                      headers=self._client.HEADERS,
                                      json=payload)

    def get_timer_records(self, timer_id, start_time: datetime, end_time: datetime):
        """
        Parameters:
            timer_id: id of the timer
            start_time: start of focus time. In UTC, so adjust accordingly!
            end_time: end of focus time. In UTC, so adjust accordingly!
        """

        url = self.POMO_BASE_URL + "/timing?from=%.0f&to=%.0f" % (
            int(start_time.timestamp() * 1000), int(end_time.timestamp() * 1000))

        response = self._client.http_get(url=url,
                                         cookies=self._client.cookies,
                                         headers=self._client.HEADERS)
        gathered_records = []
        for record in response:
            tasks = record['tasks']
            for entry in tasks:
                if "timerId" in entry and entry['timerId'] == timer_id:
                    gathered_records.append(record)

        return gathered_records

    def build_timer_record(self, start_time: datetime, end_time: datetime, timer_name=None, timer_id=None,
                           append_to: list = None):

        if timer_name is None and timer_id is None:
            raise AttributeError("Provide either task name or task id")
        if timer_name is not None:
            task = self.get_timer(self.get_timer_id_by_name(timer_name))
        else:
            task = self._client.get_by_id(timer_id)
        if 'tags' not in task:
            task['tags'] = []
        payload = [{
            "tags": task['tags'],
            "projectName": "",
            "timerId": task['id'],
            "timerName": task['name'],
            "startTime": str(start_time.isoformat() + "+0000"),
            "endTime": str(end_time.isoformat() + "+0000")
        }]

        if append_to is not None:
            append_to.append(payload[0])
            return append_to
        return payload
