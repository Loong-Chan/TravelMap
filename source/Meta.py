import json
import time


MetaFilePath = "./META.json"
Meta = None


def readMeta():
    with open(MetaFilePath, "r", encoding='utf-8') as f:
        global Meta
        Meta = json.loads(f.read())


def writeMeta():
    with open(MetaFilePath, "w", encoding="utf-8") as f:
        global Meta
        cTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        Meta["Last update"] = cTime
        json.dump(Meta, f, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    readMeta()
    writeMeta()
