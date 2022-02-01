import site
import os.path

# read version details from version.txt
def read_version():
    version_file = os.path.join(site.getsitepackages()[-1], "medhalib", "version.txt")
    with open(version_file, "r") as vfl:
        return vfl.read()

__version__=read_version()