from core import BaseModule


class Module(BaseModule):
    def __init__(self):
        super().__init__(name="time", description="负责模拟和推进时间")

    def install(self):
        pass

    def uninstall(self):
        pass

    def tick(self):
        pass
