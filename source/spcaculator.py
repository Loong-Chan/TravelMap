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
