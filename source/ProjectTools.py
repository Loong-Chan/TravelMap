from os import getcwd


def getProjectPath(currentPath: str = getcwd(), mainFolder: str = "TravelMap") -> str:
    path = currentPath.replace("\\", "/")
    pos = path.rfind(mainFolder)
    return path[:pos] + mainFolder


if __name__ == "__main__":
    print(getProjectPath())
