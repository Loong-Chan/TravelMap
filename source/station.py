# 站点


class Station:
    def __init__(self, stationName: str) -> None:
        self._name = stationName

    def getName(self) -> str:
        return self._name
