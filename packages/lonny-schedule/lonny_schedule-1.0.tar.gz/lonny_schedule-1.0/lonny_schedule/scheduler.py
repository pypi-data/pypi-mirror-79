from datetime import datetime

class Scheduler:
    def __init__(self):
        self._scheduled = list()

    def schedule(self, fn, *, interval, times = None):
        now_dt = datetime.utcnow()
        if times is None or times > 0:
            self._scheduled.insert(0, (fn, now_dt, interval, times))

    def run_next(self):
        now_dt = datetime.utcnow()
        if len(self._scheduled) == 0:
            return False
        fn, scheduled_dt, interval, times = self._scheduled[0]
        if scheduled_dt > now_dt:
            return False
        fn()
        self._scheduled.pop(0)
        new_times = None if times is None else times - 1
        if new_times is None or new_times > 0:
            self._scheduled.append((fn, now_dt + interval, interval, new_times))
            self._scheduled.sort(key = lambda t: t[1])
        return True
