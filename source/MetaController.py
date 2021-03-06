import json
import time
from ProjectTools import getProjectPath


MetaFilePath = getProjectPath() + "/META.json"

# 这个类也要是单例类才可以


class MetaController:
    def __init__(self, metaPath: str = MetaFilePath) -> None:
        self._modify = False
        self._metaFilePath = metaPath
        with open(self._metaFilePath, "r", encoding="utf-8") as mFile:
            self._meta = json.loads(mFile.read())

    def __del__(self) -> None:
        # 如果没有更新，就不用重新写一次META文件
        if not self._modify:
            return
        cTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        self._meta["Last update"] = cTime
        with open(self._metaFilePath, "w", encoding="utf-8") as mFile:
            json.dump(self._meta, mFile, indent=4, ensure_ascii=False)

    def getNameCN(self) -> None:
        return self._meta["project name CN"]

    def getNameEN(self) -> None:
        return self._meta["project name EN"]

    def getDeveloper(self) -> None:
        return self._meta["developer"]

    def getCodeVersion(self) -> None:
        return self._meta["code version"]

    def getDataVersion(self) -> None:
        return self._meta["data version"]

    def getLastUpdate(self) -> None:
        return self._meta["Last update"]

    def getGithubAddress(self) -> None:
        return self._meta["github address"]

    def update(self, item, newVaule) -> None:
        if item not in self._meta:
            print("no such item.")
            return
        self._meta[item] = newVaule
        self._modify = True


if __name__ == "__main__":
    mc = MetaController()
    mc.update("code version", "0.0.1")
    mc.update("data version", "0.0.1")
