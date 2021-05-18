# 我在想Console要设计成互斥的，就是一个文件只能开一个console，然后有了console就不用每次都要运行命令
# 而且可以分管理员模式和普通用户模式，普通用户只能查询，管理员可以添加修改，可以同时多个用户操作，但是只能有一个管理员操作


from Metro import Metro
from MetaController import MetaController
from math import ceil
import os


class MetroConsole:

    consoleWidth = 70
    password = "123456"

    def __init__(self) -> None:
        self._administrator = False
        self._file = None
        self._meta = MetaController()
        self._isAdmin = False
        # 运行控制台
        self.console()

    def console(self) -> None:
        # 首界面
        while(True):
            self.printMeta()
            print(" Please select the operation Mode(u/a):", end="")
            mode = input()
            if mode == "a":
                print("password:", end="")
                if input() == MetroConsole.password:
                    print("hello!")
                    break
            elif mode == "u":
                print("fuck you.")
                break
            else:
                os.system("cls")

    def printStr(self, string: str, shift: int = None) -> None:
        """格式化输出一行，其中shift指从左往右的位移，默认居中"""
        # 计算左空格数
        if shift is None:  # 居中的情况
            blankLenL = ceil((MetroConsole.consoleWidth - 2 - len(string)) / 2)
        else:  # 左对齐的情况
            blankLenL = shift
        # 输出字符串
        blankLenR = MetroConsole.consoleWidth - 2 - blankLenL - len(string)
        if(blankLenL <= 0 or blankLenR <= 0):
            print("error! console width too small")
            return
        print("*" + " " * blankLenL + string + " " * blankLenR + "*")

    def printMeta(self) -> None:
        os.system("cls")
        print("*" * MetroConsole.consoleWidth)
        print("*" + " " * (MetroConsole.consoleWidth - 2) + "*")
        self.printStr(self._meta.getNameEN())
        self.printStr("developer: " + self._meta.getDeveloper())
        self.printStr("version: " + self._meta.getVersion())
        print("*" + " " * (MetroConsole.consoleWidth - 2) + "*")
        print("*" * MetroConsole.consoleWidth)


if __name__ == "__main__":
    MetroConsole()
