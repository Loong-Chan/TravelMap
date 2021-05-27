from Metro import Metro
from MetaController import MetaController
from ProjectTools import getProjectPath
from Console import Console
import os


class MetroConsole(Console):

    password = "123456"

    def __init__(self) -> None:

        super(MetroConsole, self).__init__()

        self._file = None
        self._meta = MetaController()
        self._metro = None

    def define(self) -> None:
        self.newPage(self.pageMain, "Main")
        self.newPage(self.pageAdmin, "Admin")
        self.newPage(self.pageUser, "User")
        self.setJump("Main")

    def printMeta(self) -> None:
        self.newBox()
        self.addContentToBox(self._meta.getNameEN())
        self.addContentToBox("developer: " + self._meta.getDeveloper())
        self.addContentToBox("code version: " + self._meta.getCodeVersion())
        self.addContentToBox("data version: " + self._meta.getDataVersion())
        self.drawBox()

    def printAdminHint(self) -> None:
        self.newBox()
        self.addContentToBox("logout: lot out and return to the main interface", 5)
        self.addContentToBox("list  : list the infomation of the designated station or line", 5)
        self.addContentToBox("new   : build a new station or line", 5)
        self.addContentToBox("add   : add a station to a line:", 5)
        self.addContentToBox("save  : save the latest data to a file", 5)
        self.addContentToBox("load  : load an existing data file", 5)
        self.addContentToBox("create: create a new data file", 5)
        self.addContentToBox("query : query the line between any station", 5)
        self.drawBox()

    def printUserHint(self) -> None:
        self.newBox()
        self.addContentToBox("logout: lot out and return to the main interface", 5)
        self.addContentToBox("list  : list the infomation of the designated station or line", 5)
        self.addContentToBox("load  : load an existing data file", 5)
        self.addContentToBox("query : query the line between any station", 5)
        self.drawBox()

    def pageMain(self, pageIndex: int) -> None:

        vaildOper = {"user": self.operTurnToUser, "admin": self.operTurnToAdmin,
                     "exit": self.operExit}

        while pageIndex == self._select:
            os.system("cls")
            self.printMeta()
            print("\n Please select the operation Mode(user/admin):", end="")
            oper, argList = self.inputOper()
            self.dispatcher(oper, argList, vaildOper)

    def pageUser(self, pageIndex: int) -> None:

        vaildOper = {"logout": self.operLogout, "list": self.operList,
                     "new": self.operNew, "add": self.operAdd,
                     "save": self.operSave, "load": self.operLoad,
                     "create": self.operCreate, "query": self.operQuery}

        os.system("cls")
        self.printUserHint()
        print("\n Enter you operation:", end="")
        while pageIndex == self._select:
            oper, argList = self.inputOper()
            os.system("cls")
            self.printUserHint()
            self.dispatcher(oper, argList, vaildOper)
            print("\n Enter you operation:", end="")

    def pageAdmin(self, pageIndex: int) -> None:

        vaildOper = {"logout": self.operLogout, "list": self.operList,
                     "load": self.operLoad, "query": self.operQuery}

        os.system("cls")
        self.printAdminHint()
        print("\n Enter you operation:", end="")
        while pageIndex == self._select:
            oper, argList = self.inputOper()
            os.system("cls")
            self.printAdminHint()
            self.dispatcher(oper, argList, vaildOper)
            print("\n Enter you operation:", end="")

    def operTurnToUser(self, argList: list):
        self.setJump("User")

    def operTurnToAdmin(self, argList: list):
        print(" Please enter your password:", end="")
        if input() == MetroConsole.password:
            self.setJump("Admin")

    def operLogout(self, argList: list):
        self.setJump("Main")

    def operList(self, argList: list):

        if self._file is None:
            print(" You haven't opened a file yet.")
            return None

        stationNames = self._metro.getStationsName()
        lineNames = self._metro.getLinesName()
        stationOrder = self._metro.getStationOrder()

        self.newBox()
        for i in range(len(lineNames)):
            self.addContentToBox("line: {}".format(lineNames[i]), 5)
            for j in stationOrder[i]:
                self.addContentToBox("{}-->".format(stationNames[j]), 10)
        self.drawBox()

    def operLoad(self, argList: list):

        if self._file is not None:
            print(" You have already opened a file.")
            return None

        if len(argList) < 1:
            print(" Wrong number of parameters.")
            print(" Usage: load -<city name>")
            return None

        filePath = getProjectPath() + "/citys/{}.txt".format(argList[0])
        if not os.path.exists(filePath):
            print(" File doesn't exist.")
            return None

        print(" Load data from file: {}...".format(filePath), end="")
        self._metro = Metro(filePath)
        print(" done!")

    def operQuery(self, argList: list):

        if self._file is None:
            print(" You haven't opened a file yet.")
            return None

        if len(argList) < 2:
            print(" Wrong number of parameters.")
            print(" Usage: load -<station name 1> -<station name 2>")
            return None

        stationNames = self._metro.getStationsName()
        path, weight = self._metro.findPath(argList[0], argList[1])

        self.newBox()
        self.addContentToBox("You need to take {} stops in the subway".format(weight), 5)
        for s in path:
            self.addContentToBox("{}-->".format(stationNames[s]), 10)
        self.drawBox()

    def operNew(self, argList: list):
        pass

    def operAdd(self, argList: list):
        pass

    def operSave(self, argList: list):
        pass

    def operCreate(self, argList: list):
        pass


if __name__ == "__main__":
    MetroConsole().startUp()
