class PomoManager:
    POMO_BASE_URL = 'https://api.ticktick.com/api/v2/pomodoros'
    POMO_BASE_URL2 = 'https://api.ticktick.com/api/v2/pomodoro'
    POMO_PREFERENCES_URL = 'https://api.ticktick.com/api/v2/user/preferences/pomodoro'
    POMO_STATISTIC_URL = POMO_BASE_URL + "/statistics/generalForDesktop"  # mobile platform might provide additional information

    def __init__(self, client_class):
        self._client = client_class
        self.access_token = ''

    def statistics(self):
        # https://api.ticktick.com/api/v2/statistics/general
        pass

    def delete(self, record_id):
        """
        Deletes the given record.
        Arguments:
            record_id: The internal id of the record entry
        """
        return self._client.http_delete(url=self.POMO_BASE_URL2 + "/" + record_id,
                                        cookies=self._client.cookies,
                                        headers=self._client.HEADERS)

    def record(self):
        """
        Records of all pomo AND focus sessions.
        !!! This implementation seems to be limited to the record of the last month.
        Returns:


        """
        response = self._client.http_get(url=self.POMO_BASE_URL + "/timeline",
                                         cookies=self._client.cookies,
                                         headers=self._client.HEADERS)
        return response

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

        return self._client.http_put(url=self.POMO_PREFERENCES_URL,
                                     cookies=self._client.cookies,
                                     headers=self._client.HEADERS,
                                     json=payload)
