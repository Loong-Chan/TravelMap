# 线路
class Line:
    def __init__(self, lineName: str) -> None:
        self._name = lineName

    def getName(self) -> str:
        return self._name
