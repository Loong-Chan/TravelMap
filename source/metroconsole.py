# 我在想Console要设计成互斥的，就是一个文件只能开一个console，然后有了console就不用每次都要运行命令
# 而且可以分管理员模式和普通用户模式，普通用户只能查询，管理员可以添加修改，可以同时多个用户操作，但是只能有一个管理员操作


class MetroConsole:
    def __init__(self) -> None:
        self._administrator = False
        self._file = None
        self.console()

    def console(self) -> None:
        pass
