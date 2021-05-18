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
        self._vaildOperMain = {"admin": self.operAdmin, "user": self.operUser, "exit": self.operExit}
        self._vaildOperAdmin = {"logout": None, "list": None, "open": None, "query": None}
        self._vaildOperUser = {"logout": None, "list": None, "new": None, "add": None, "save": None,
                               "open": None, "create": None, "query": None}
        # 运行控制台
        self.console()

    def console(self) -> None:
        # 首界面
        while(True):
            os.system("cls")
            self.printMeta()
            print(" Please select the operation Mode(user/admin):", end="")
            oper, args = self.inputOper()
            if self.dispatcher(oper, args, self._vaildOperMain):
                break
        # 操作介绍界面
        os.system("cls")
        self.printHint()
        oper = input()

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
        """输出主界面中的软件的元信息"""
        print("*" * MetroConsole.consoleWidth)
        print("*" + " " * (MetroConsole.consoleWidth - 2) + "*")
        self.printStr(self._meta.getNameEN())
        self.printStr("developer: " + self._meta.getDeveloper())
        self.printStr("code version: " + self._meta.getCodeVersion())
        self.printStr("data version: " + self._meta.getDataVersion())
        print("*" + " " * (MetroConsole.consoleWidth - 2) + "*")
        print("*" * MetroConsole.consoleWidth)

    def printHint(self) -> None:
        """输出使用界面中的提示操作信息"""
        print("*" * MetroConsole.consoleWidth)
        print("*" + " " * (MetroConsole.consoleWidth - 2) + "*")
        self.printStr("logout: lot out and return to the main interface", 5)
        self.printStr(
            "list  : list the infomation of the designated station or line", 5)
        self.printStr("new   : build a new station or line", 5)
        self.printStr("add   : add a station to a line:", 5)
        self.printStr("save  : save the latest data to a file", 5)
        self.printStr("open  : open an existing data file", 5)
        self.printStr("create: create a new data file", 5)
        self.printStr("query : query the line between any station", 5)
        print("*" + " " * (MetroConsole.consoleWidth - 2) + "*")
        print("*" * MetroConsole.consoleWidth)
        print(" enter you operation:", end="")

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

    def operAdmin(self, args: list) -> bool:
        self._isAdmin = True
        return True

    def operUser(self, args: list) -> bool:
        self._isAdmin = False
        return True

    def operExit(self, args: list) -> None:
        exit(0)

    def operDefault(self, args: list) -> bool:
        return False




if __name__ == "__main__":
    MetroConsole()

