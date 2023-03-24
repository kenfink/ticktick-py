from datetime import datetime
import secrets


class PomoManager:
    POMO_BASE_URL = 'https://api.ticktick.com/api/v2/pomodoros'
    POMO_BASE_URL2 = 'https://api.ticktick.com/api/v2/pomodoro'
    POMO_PREFERENCES_URL = 'https://api.ticktick.com/api/v2/user/preferences'
    # mobile platform might provide additional information
    POMO_BATCH_URL = "https://api.ticktick.com/api/v2/batch/pomodoro"

    def __init__(self, client_class):
        self._client = client_class
        self.access_token = ''

    def get_today(self):
        """
        Returns:
            dict containing the pomo statistics for today, times in minutes
        """
        return self._client.http_get(url=self.POMO_BASE_URL + "/statistics/generalForDesktop",
                                     cookies=self._client.cookies,
                                     headers=self._client.HEADERS)

    def add(self, tasks: list, start_time: datetime, pause_duration=0, end_time: datetime = datetime.now(), status=1,
            note=""):
        generated_id = secrets.token_hex(24)
        payload = {
            "add": [
                {
                    "id": generated_id,
                    "startTime": start_time.isoformat() + "+0000",
                    "endTime": end_time.isoformat() + "+0000",
                    "status": status,
                    "pauseDuration": pause_duration,
                    "tasks": tasks,
                    "note": note
                }
            ],
            "update": []
        }

        print(payload)
        return self._client.http_post(url=self.POMO_BATCH_URL,
                                      cookies=self._client.cookies,
                                      headers=self._client.HEADERS,
                                      json=payload)

    def build_record(self, start_time: datetime, end_time: datetime, task_name=None, task_id=None,
                     append_to: list = None):
        if task_name is None and task_id is None:
            raise AttributeError("Provide either task name or task id")
        if task_name is not None:
            task = self._client.get_by_fields(title=task_name)
        else:
            task = self._client.get_by_id(task_id)
        project = self._client.get_by_id(task['projectId'])
        if 'tags' not in task:
            task['tags'] = []
        payload = [{
            "taskId": task['id'],
            "title": task['title'],
            "tags": task['tags'],
            "projectName": project['name'],
            "startTime": start_time.isoformat() + "+0000",
            "endTime": end_time.isoformat() + "+0000"
        }]

        if append_to is not None:
            append_to.append(payload[0])
            return append_to
        return payload

    def delete(self, record_id):
        """
        Deletes the given record.
        Arguments:
            record_id: The internal id of the record entry
        """
        return self._client.http_delete(url=self.POMO_BASE_URL2 + "/" + record_id,
                                        cookies=self._client.cookies,
                                        headers=self._client.HEADERS)

    def get_timeline(self):
        """
        Records of all pomo AND focus sessions.
        !!! This implementation seems to be limited to the record of the last 10 days.
        Returns:
            Record entries: [
            {id:record-id,
            tasks[
                {taskId:task-id,
                title:task title,
                projectName:project / list name,
                tags:[],
                startTime: ISO 8601 start time,
                endTime: ISO 8601 end time},

                ...,
            ],
            startTime: ISO 8601 start time of the record
            endTime: ISO 8601 end time of the record
            status: status
            pauseDuration: pause duration in seconds
            etag: internal tag
            type: type
            added: boolean},

            ...]
        """
        # TODO add functionality to view complete record.
        # https://api.ticktick.com/api/v2/pomodoros/timeline?to=MILLIS seems to return the 10 days prior to the stamp

        response = self._client.http_get(url=self.POMO_BASE_URL + "/timeline",
                                         cookies=self._client.cookies,
                                         headers=self._client.HEADERS)
        return response

    def get_preferences(self):
        """
        Returns:
            dict:
            {
                "id": internal id,
              "shortBreakDuration": Duration of short breaks in minutes,
              "longBreakDuration": Duration of long breaks in minutes,
              "longBreakInterval": Interval of long breaks,
              "pomoGoal": Daily pomo goal,
              "focusDuration": Daily focus goal,
              "mindfulnessEnabled": boolean,
              "autoPomo": Auto start focus,
              "autoBreak": Auto start break,
              "lightsOn": Lights on,
              "focused": boolean,
              "soundsOn": sound boolean,
              "pomoDuration": Duration of pomo focus sessions in minutes
            }
        """
        return self._client.http_get(url=self.POMO_PREFERENCES_URL + "/pomodoro",
                                     cookies=self._client.cookies,
                                     headers=self._client.HEADERS)

    def set_preferences(self,
                        sound=True,
                        long_break_interval=4,
                        focus_duration=120,
                        auto_break=False,
                        auto_pomo=False,
                        pomo_goal=4,
                        pomo_duration=20,
                        short_break_duration=5,
                        long_break_duration=15,
                        mindfulness_enabled=False):
        """
        Updates the pomo AND focus preferences.

        Arguments:
            sound: Whether finishing a session should notify the user with a sound
            long_break_interval: (pomo) Interval for long breaks
            focus_duration: Daily target focus time in minutes (pomos count towards this target)
            auto_break: Whether breaks should automatically start after a pomo focus session finishes
            auto_pomo: Whether a pomo focus session should automatically start after a break ends
            pomo_goal: Daily pomo focus session goal
            pomo_duration: Duration of pomo focus sessions in minutes
            short_break_duration: Duration of short breaks in minutes
            long_break_duration: Duration of long breaks in minutes
            mindfulness_enabled: TODO check if used at all
        """

        payload = {
            "soundsOn": sound,
            "longBreakInterval": long_break_interval,
            "focusDuration": focus_duration,
            "autoBreak": auto_break,
            "autoPomo": auto_pomo,
            "pomoGoal": pomo_goal,
            "pomoDuration": pomo_duration,
            "shortBreakDuration": short_break_duration,
            "longBreakDuration": long_break_duration,
            "mindfulnessEnabled": mindfulness_enabled
        }

        return self._client.http_put(url=self.POMO_PREFERENCES_URL + "/pomodoro",
                                     cookies=self._client.cookies,
                                     headers=self._client.HEADERS,
                                     json=payload)
