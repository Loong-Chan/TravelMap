# 设计这个类的初衷是想把算法的实现完全抽象出来不受业务逻辑的干扰
# 因此不想在SPCaulotor这个类中加入类似 self._inited 和 self._caculator 这种变量
# 另外我希望为我在将来想继续实现的功能留下可以拓展的空间，比如：
# 1.根据场景可以采用多种算法,不同格式的加载
# 2.把算法的中间结果储存成文件，只要输入的数据没有改变，就不要重复计算
# 3.甚至可以把caculator写成单例，减少内存占用
# 4.我还在考虑是否能把这个控制类写成装饰类
# 5.现在在目前功能需求非常简单的时候，这个类显得非常鸡肋

from SPCaculator import SPCaculator


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
