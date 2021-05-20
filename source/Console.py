#  我希望把这个类设计成MetroConsole类的父类，这个类内置实现一个console的基本绘制，页面跳转，可选操作的集合，操作的装饰器，线程控制等功能
#  这个的实现我放在重构里面，目前还是对这玩意的具体实现不清楚


from math import ceil


class Console:
    # 目前只支持纯英文

    def __init__(self, width: int = 70) -> None:
        self._width = width
        self._pageBuffer = ""

    def newDiv(self) -> None:
        self._pageBuffer = ""

    # 希望能实现处理超长自动分成多行输出的情况
    def addContentToDiv(self, content: str, alignment: int = None) -> None:

        if len(content) > self._width - 2 or (alignment is not None and alignment >= self._width - 2):
            raise Exception()

        if alignment is None:
            blankLenL = ceil((self._width - 2 - len(content)) / 2)
        else:
            blankLenL = alignment
        blankLenR = self._width - 2 - blankLenL - len(content)

        self._pageBuffer += ("*" + " " * blankLenL + content + " " * blankLenR + "*\n")

    def drawDiv(self) -> None:
        self._pageBuffer = "*" + " " * (self._width - 2) + "*\n" + self._pageBuffer
        self._pageBuffer = "*" * self._width + "\n" + self._pageBuffer
        self._pageBuffer = self._pageBuffer + "*" + " " * (self._width - 2) + "*\n"
        self._pageBuffer = self._pageBuffer + "*" * self._width + "\n"
        print(self._pageBuffer)

    def pageManager(self) -> None:
        pass


if __name__ == "__main__":
    c = Console()
    c.newDiv()
    c.addContentToDiv("hello")
    c.addContentToDiv("fuckyou")
    c.drawPage()
