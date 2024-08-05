import datetime
import time

import core
from core import BaseModule
from modules.time import TIME


class Module(BaseModule):
    def __init__(
        self,
        interval_second: float = None,
        start_datetime: datetime.datetime = None,
        add_days: int = None,
    ):
        super().__init__(name="time", description="负责模拟和推进时间")
        self.interval_second = core.default_value(interval_second, 0.0167)
        self.cur_time = core.default_value(start_datetime, datetime.datetime(1, 1, 1))
        self.add_days = core.default_value(add_days, 1)
        core.data_store.set(TIME, self.cur_time)

    def install(self):
        pass

    def uninstall(self):
        pass

    def tick(self):
        time.sleep(self.interval_second)
        self.cur_time += datetime.timedelta(days=self.add_days)
        core.data_store.set(TIME, self.cur_time)
