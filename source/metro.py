from Line import Line
from Station import Station
from SPCaculatorController import SPCaculatorController


# 地铁
class Metro:
    """地铁类"""
    def __init__(self, filePath: str = None) -> None:
        self._stationCount = 0  # 站点总数量
        self._lineCount = 0  # 线路总数量
        self._stations = []  # 存储所有站点的实例
        self._lines = []  # 存储所有线路的实例
        self._stationNameToNumber = {}  # 根据站点名查找下标
        self._lineNameToNumber = {}  # 根据线路名字查找下标
        self._stationOrder = []  # 记录每一条线路中的站点次序
        self._caculator = SPCaculatorController()  # 通过这个调用计算资源计算站点之间的最短路径
        # 可以选择从已有的文件中读取信息
        if filePath is not None:
            with open(filePath, "r") as f:
                # 读取站点信息
                self._stationCount = int(f.readline().strip('\n'))  # 读取站点总数量
                for i in range(self._stationCount):
                    stationName = f.readline().strip('\n')  # 读取每个站点的名称
                    self._stations.append(Station(stationName))
                    self._stationNameToNumber[stationName] = i
                # 读取线路信息
                self._lineCount = int(f.readline().strip('\n'))  # 读取线路总数量
                for i in range(self._lineCount):
                    lineName = f.readline().strip('\n')  # 读取每条线路的名称
                    self._lines.append(Line(lineName))
                    self._lineNameToNumber[lineName] = i
                    self._stationOrder.append([])
                    stationNum = int(f.readline().strip('\n'))  # 读取该线路经过站点的数量
                    for i in range(stationNum):
                        stationName = f.readline().strip('\n')  # 读取该线路经过的所有站点的名称
                        self.addStationToLine(stationName, lineName)
        # 通知最短路径计算器控制器：站点或者线路信息已发生更改
        self._caculator.setObsolete()

    def newStation(self, stationName: str) -> None:
        """创建新的站点"""
        # 有重名站点时不重新创建
        if stationName in self._stationNameToNumber:
            print("warning: [%s] has existed." % (stationName))
            return
        self._stations.append(Station(stationName))
        self._stationNameToNumber[stationName] = self._stationCount
        self._stationCount += 1
        # 通知最短路径计算器控制器：站点或者线路信息已发生更改
        self._caculator.setObsolete()

    def newLine(self, lineName: str) -> None:
        """创建新的线路"""
        # 有重名线路时不重新创建
        if lineName in self._lineNameToNumber:
            print("warning: [%s] has existed." % (lineName))
            return
        self._lines.append(Line(lineName))
        self._lineNameToNumber[lineName] = self._lineCount
        self._lineCount += 1
        self._stationOrder.append([])
        # 通知最短路径计算器控制器：站点或者线路信息已发生更改
        self._caculator.setObsolete()

    def addStationToLine(self, stationName: str, lineName: str, order: int = None) -> None:
        """把一个已有站点添加进一条已有线路中"""
        # 检查站点是否存在
        if stationName not in self._stationNameToNumber:
            print("addStationToLine() error: no such station(%s)." % (stationName))
            return
        # 检查线路是否存在
        if lineName not in self._lineNameToNumber:
            print("addStationToLine() error: no such line(%s)." % (lineName))
            return
        # 检查order是否合法
        lineNO = self._lineNameToNumber[lineName]
        if order is None:
            order = len(self._stationOrder[lineNO])
        if order < 0 or order > len(self._stationOrder[lineNO]):
            print("addStationToLine() error: order illegal.")
            return
        # 检查该站点是否已经在该线路中
        stationNO = self._stationNameToNumber[stationName]
        if stationNO in self._stationOrder[lineNO]:
            print("addStationToLine() error: %s has been in %s." % (stationName, lineName))
            return
        # 把该站点标记为该线路会经过的站点
        self._stationOrder[lineNO].insert(order, stationNO)
        # 通知最短路径计算器控制器：站点或者线路信息已发生更改
        self._caculator.setObsolete()

    def writeToFile(self, filePath: str) -> None:
        """把当前内存中的铁路信息写入文件中"""
        # 文件中的数据会被全部覆盖
        print("The original data in the file(%s) will be overwritten." % (filePath))
        # 写入信息
        with open(filePath, "w") as f:
            # 写入站点信息
            f.write("%d\n" % (self._stationCount))  # 站点总数量
            for station in self._stations:
                f.write("%s\n" % (station.getName()))  # 每个站点的名称
            # 写入线路信息
            f.write("%d\n" % (self._lineCount))  # 线路总数量
            for line in self._lines:
                f.write("%s\n" % (line.getName()))  # 每条线路的名称
                lineNO = self._lineNameToNumber[line.getName()]  # 该线路经过的站点的数量
                f.write("%d\n" % len(self._stationOrder[lineNO]))
                for stationNO in self._stationOrder[lineNO]:
                    f.write("%s\n" % (self._stations[stationNO].getName()))  # 该线路经过的每个站点的名称

    def printInfo(self) -> None:
        """输出当前所有铁路信息"""
        # 输出站点信息
        print("station number:%d" % (self._stationCount))  # 输出站点总数量
        for i in range(self._stationCount):
            print("[%s]" % (self._stations[i].getName()), end="  ")  # 输出所有站点的名称
            if(i % 10 == 9):
                print("")
        # 输出线路信息
        print("\nline number:%d" % (self._lineCount))  # 输出线路的总数量
        for i in range(self._lineCount):
            lineName = self._lines[i].getName()
            lineNO = self._lineNameToNumber[lineName]
            print("line name: %s, " % (lineName), end="")  # 输出线路的名称
            print("%d station(s) on the way." % (len(self._stationOrder[lineNO])))  # 输出该线路经过站点的数量
            for stationNO in self._stationOrder[lineNO]:
                print("[%s]---" % (self._stations[stationNO].getName()), end="")  # 输出该线路经过站点的名称
            print("\b\b\b   ")

    def getStationOrder(self) -> list:
        """返回以数组形式存储的铁路站点信息"""
        return self._stationOrder

    def getStationCount(self) -> int:
        """返回站点总数"""
        return self._stationCount

    def getLineCount(self) -> int:
        """返回线路总数"""
        return self._lineCount

    def findPath(self, stationName1: str, stationName2: str) -> None:
        """打印出任意两个站点之间的最佳通行方式"""
        if (stationName1 not in self._stationNameToNumber) or (stationName2 not in self._stationNameToNumber):
            print("error: no such station.")
            return
        if not self._caculator.getInited():
            self._caculator.loadCaculator("MetroLines", self._stationOrder, self._stationCount)
        no1 = self._stationNameToNumber[stationName1]
        no2 = self._stationNameToNumber[stationName2]
        path, weight = self._caculator.getShortestPath(no1, no2)
        print("from %s to %s:" % (stationName1, stationName2))
        print("path: ", end="")
        for s in path:
            print("%s-->" % (self._stations[s].getName()), end="")
        print("\b\b\b   ")
        print("weight: %d" % weight)


if __name__ == "__main__":
    guangzhou = Metro("./guangzhou.txt")
    guangzhou.findPath("Chebei", "Chebeinan")
