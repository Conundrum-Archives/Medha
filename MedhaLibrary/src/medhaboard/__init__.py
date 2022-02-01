# read version details from version.txt
def read_version():
    with open("version.txt", "r") as vfl:
        return vfl.read()

__version__=read_version()