#  我希望把这个类设计成MetroConsole类的父类，这个类内置实现一个console的基本绘制，页面跳转，可选操作的集合，操作的装饰器，线程控制等功能
#  这个的实现我放在重构里面，目前还是对这玩意的具体实现不清楚


from math import ceil


class Console:
    # 目前只支持纯英文

    def __init__(self, width: int = 70) -> None:
        self._width = width
        self._boxBuffer = ""
        self._pages = []
        self._select = 0

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
        print(self._boxBuffer)

    def pageManager(self) -> None:
        while(True):
            self._pages[self._select](self._select)

    def newPage(self, pageFunc) -> int:
        if not callable(pageFunc):
            raise Exception()
        self._pages.append(pageFunc)
        return len(self._pages) - 1

    def setJump(self, pageIndex: int) -> None:
        self._select = pageIndex

    def inputOper(self) -> list:
        '''从键盘读取一次操作及其参数'''
        paras = [p.strip() for p in input().split(" -")]
        return paras[0], paras[1:]

    def dispatcher(self, oper: str, args: list, vaildOper: dict) -> bool:
        """通过分派器把对应的操作和参数分派给指定函数执行"""
        if oper not in vaildOper:
            return self.operDefault(args)
        else:
            return vaildOper[oper](args)

    def pageExample(self, pageIndex: int) -> None:
        vaildOper = {"a": self.examFunc1, "b": self.examFunc2}

        '''
        xxx
        '''

        while pageIndex == self._select:
            '''
            xxx
            '''
            oper, args = self.inputOper()
            self.dispatcher(oper, args, self._vaildOperUser)

    # 在初始化时需要有一个默认页，只有退出的功能，每次退出程序都不是直接退出，而是跳转到默认页，由默认页执行退出任务
    def pageExit(self) -> None:
        pass


    def examFunc1(self, args: list) -> None:
        print(args[0])
        print(args[1])
        self.setJump(1)


if __name__ == "__main__":
    c = Console()
    c.newDiv()
    c.addContentToDiv("hello")
    c.addContentToDiv("fuckyou")
    c.drawPage()
