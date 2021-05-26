#  我希望把这个类设计成MetroConsole类的父类，这个类内置实现一个console的基本绘制，页面跳转，可选操作的集合，操作的装饰器，线程控制等功能
#  这个的实现我放在重构里面，目前还是对这玩意的具体实现不清楚


from math import ceil
from abc import ABC, abstractmethod


class Console(ABC):
    # 目前只支持纯英文

    def __init__(self, width: int = 70) -> None:
        self._width = width
        self._boxBuffer = ""
        self._pages = [self.pageExit]
        self._select = 0
        self._pageNameToIndex = {"Exit": 0}

    def newBox(self) -> None:
        self._boxBuffer = ""

    # 希望能实现处理超长自动分成多行输出的情况
    def addContentToBox(self, content: str, alignment: int = None) -> None:

        if len(content) > self._width - 2 or (alignment is not None and alignment >= self._width - 2):
            raise Exception()

        if alignment is None:
            blankLenL = ceil((self._width - 2 - len(content)) / 2)
        else:
            blankLenL = alignment
        blankLenR = self._width - 2 - blankLenL - len(content)

        self._boxBuffer += ("*" + " " * blankLenL + content + " " * blankLenR + "*\n")

    def drawBox(self) -> None:
        self._boxBuffer = "*" + " " * (self._width - 2) + "*\n" + self._boxBuffer
        self._boxBuffer = "*" * self._width + "\n" + self._boxBuffer
        self._boxBuffer = self._boxBuffer + "*" + " " * (self._width - 2) + "*\n"
        self._boxBuffer = self._boxBuffer + "*" * self._width + "\n"
        print(self._boxBuffer, end="")

    def startUp(self) -> None:
        self.define()
        while(True):
            self._pages[self._select](self._select)

    def newPage(self, pageFunc, pageName: str) -> int:
        if not callable(pageFunc) or pageFunc.__code__.co_argcount == 0:
            raise Exception("page is not in the right format.")
        if pageName in self._pageNameToIndex:
            raise Exception("page name has been used.")

        self._pageNameToIndex[pageName] = len(self._pages)
        self._pages.append(pageFunc)

        return self._pageNameToIndex[pageName]

    def setJump(self, pageInfo) -> None:
        if isinstance(pageInfo, int):
            if pageInfo >= len(self._pages):
                raise Exception("Index out of range.")
            self._select = pageInfo
            return
        if isinstance(pageInfo, str):
            if pageInfo not in self._pageNameToIndex:
                raise Exception("no such page name")
            self._select = self._pageNameToIndex[pageInfo]
            return
        raise Exception("page info type error.")

    def inputOper(self) -> list:
        '''从键盘读取一次操作及其参数'''
        paras = [p.strip() for p in input().split(" -")]
        return paras[0], paras[1:]

    def dispatcher(self, oper: str, argList: list, vaildOper: dict) -> bool:
        """通过分派器把对应的操作和参数分派给指定函数执行"""
        if oper not in vaildOper:
            return self.operDefault(argList)
        else:
            return vaildOper[oper](argList)

    # 在初始化时需要有一个默认页，只有退出的功能，每次退出程序都不是直接退出，而是跳转到默认页，由默认页执行退出任务
    def pageExit(self, pageIndex: int) -> None:
        exit(0)

    def operExit(self, argList: list):
        self.setJump(0)

    def operDefault(self, argList) -> None:
        return None

    @abstractmethod
    def define(self) -> None:
        pass


'''
    def pageExample(self, pageIndex: int) -> None:
        vaildOper = {"a": self.examFunc1, "b": self.examFunc2}


        # xxx


        while pageIndex == self._select:

            # xxx

            oper, args = self.inputOper()
            self.dispatcher(oper, args, self._vaildOperUser)

    def examFunc1(self, args: list) -> None:
        print(args[0])
        print(args[1])
        self.setJump(1)
'''

if __name__ == "__main__":
    c = Console()
    c.newDiv()
    c.addContentToDiv("hello")
    c.addContentToDiv("fuckyou")
    c.drawPage()
