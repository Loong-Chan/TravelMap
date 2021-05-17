'''
将来的改进方向
1. 随着算法的进一步复杂（优化空间复杂度，考虑并行计算），可以考虑把图类的管理层和业务层也分成两个类
2. 加入日志和版本管理系统
3. 把图的计算结果也作为文件存下来
4. 加密？MD5？
5. 客户端和服务端
6. 加上前端开发，做成完整的项目
7. 装进容器内？
8. 可以把接口留好，但是不要过度设计！
'''


# 站点
class Station:
    def __init__(self, stationName: str) -> None:
        self._name = stationName

    def getName(self) -> str:
        return self._name


# 线路
class Line:
    def __init__(self, lineName: str) -> None:
        self._name = lineName

    def getName(self) -> str:
        return self._name


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


# 这个类只专注算法逻辑，什么控制都不要加
class SPCaculator:
    """最短路径计算器"""
    INF = 1e10  # 路径权重的最大值

    def __init__(self) -> None:
        pass

    def initByMetroLines(self, mLines: list, stationNum: int) -> None:
        """通过以数组的方式记录的地铁线路初始化最短路径计算器"""
        # 初始化顶点总数
        self._size = stationNum
        # 初始化任两点最短路径的权重和
        self._weightMatrix = [[SPCaculator.INF] * self._size for i in range(self._size)]
        for i in range(self._size):
            self._weightMatrix[i][i] = 0
        for line in mLines:
            for i in range(len(line) - 1):
                self._weightMatrix[line[i]][line[i + 1]] = 1
                self._weightMatrix[line[i + 1]][line[i]] = 1
        # 初始化任两点最短路径的记录
        self._pathMatrix = [[i for i in range(self._size)] for j in range(self._size)]

    def computeAllSP(self) -> None:
        """计算任意两点之间的最短路径"""
        # 使用floyd算法计算所有点之间的最短路径
        for k in range(self._size):
            for i in range(self._size):
                for j in range(self._size):
                    if self._weightMatrix[i][j] > self._weightMatrix[i][k] + self._weightMatrix[k][j]:
                        self._weightMatrix[i][j] = self._weightMatrix[i][k] + self._weightMatrix[k][j]
                        # 更新路径记录
                        self._pathMatrix[i][j] = self._pathMatrix[i][k]

    def getSPWeight(self, vertex1: int, vertex2: int) -> int:
        """获取任意两点之间的最短路径权重和"""
        return self._weightMatrix[vertex1][vertex2]

    def getSPPath(self, vertex1: int, vertex2: int) -> list:
        """获取任意两点之间的最短路径"""
        shortestPath = [vertex1]
        current = vertex1
        while(current != vertex2):
            current = self._pathMatrix[current][vertex2]
            shortestPath.append(current)
        return shortestPath


# 设计这个类的初衷是想把算法的实现完全抽象出来不受业务逻辑的干扰
# 因此不想在SPCaulotor这个类中加入类似 self._inited 和 self._caculator 这种变量
# 另外我希望为我在将来想继续实现的功能留下可以拓展的空间，比如：
# 1.根据场景可以采用多种算法,不同格式的加载
# 2.把算法的中间结果储存成文件，只要输入的数据没有改变，就不要重复计算
# 3.甚至可以把caculator写成单例，减少内存占用
# 4.我还在考虑是否能把这个控制类写成装饰类
# 5.现在在目前功能需求非常简单的时候，这个类显得非常鸡肋

class SPCaculatorController:
    """最短路径计算器的控制器"""
    allDataType = ("MetroLines", )  # 最短路径计算器的所有数据加载形式

    def __init__(self) -> None:
        self._inited = False  # 最短路径计算器是否已经被初始化
        self._computed = False  # 最短路径计算器是否已经执行计算
        self._caculator = SPCaculator()  # 最短路径计算器的实例
        self._dataType = None  # 最短路径器的数据加载形式
        self._loadFunc = {"MetroLines": self._caculator.initByMetroLines}  # 数据加载形式与的加载方法

    def loadCaculator(self, dataType: str, *args: tuple) -> None:
        '''
        用不同的数据形式加载最短路径计算器
        dataType: "MetroLines", *args: (mLines: list, stationNum: int)
        '''
        if dataType not in SPCaculatorController.allDataType:
            print("error: no such data type.")
            return
        # 目前只有这一种加载形式
        if dataType == "MetroLines":
            self._dataType = dataType
            self._loadFunc[dataType](args[0], args[1])
            self._inited = True

    def compute(self) -> None:
        """对加载后的最短路径计算机执行计算"""
        if not self._inited:
            print("error: not initialize yet.")
            return
        self._caculator.computeAllSP()
        self._computed = True

    def setObsolete(self) -> None:
        """设置该最短路径计算器的数据已经过时，需要重新加载和计算"""
        self._inited = False
        self._computed = False
        self._dataType = None

    def getShortestPath(self, station1: int, station2: int) -> tuple:
        """最短路径计算器经过加载和计算后，可以获取任意两点之间的最短路径"""
        if not self._inited:
            print("error: not initialize yet.")
            return
        if not self._computed:
            self._caculator.computeAllSP()
            self._computed = True
        path = self._caculator.getSPPath(station1, station2)
        weight = self._caculator.getSPWeight(station1, station2)
        return (path, weight)

    def getInited(self) -> bool:
        """返回：最短路径计算器是否已经初始化（加载）"""
        return self._inited

    def getComputed(self) -> bool:
        """返回：最短路径计算器是否已经执行计算"""
        return self._computed


# 我在想Console要设计成互斥的，就是一个文件只能开一个console，然后有了console就不用每次都要运行命令
# 而且可以分管理员模式和普通用户模式，普通用户只能查询，管理员可以添加修改，可以同时多个用户操作，但是只能有一个管理员操作
class MetroConsole:
    def __init__(self) -> None:
        self._administrator = False
        self._file = None
        self.console()

    def console(self) -> None:
        pass


class Log:
    pass


if __name__ == "__main__":
    MetroConsole()


# https://blog.csdn.net/weixin_39956356/article/details/80620667?utm_medium=distribute.pc_relevant.none-task-blog-2%7Edefault%7EBlogCommendFromMachineLearnPai2%7Edefault-1.control&depth_1-utm_source=distribute.pc_relevant.none-task-blog-2%7Edefault%7EBlogCommendFromMachineLearnPai2%7Edefault-1.control
