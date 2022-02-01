import os
import shutil
import datetime
from setuptools import setup, find_packages

# build directory
distdir = "dist"

# cleanup if exist before build
if (os.path.exists(distdir)):
  print("cleaning {}".format(distdir))
  shutil.rmtree(distdir)

# timestampted version suffix
build_datetime = datetime.datetime.now()
version = '2.0.' + build_datetime.strftime("%Y%m%d.%H%M%S")
print("version: {}".format(version))

# write build details to version.txt
with open(os.path.join("src", "medhaboard", "version.txt"), "w") as vfl:
    details = """
    Version: {version}
    Date: {date}
    """.format(version=version, date=build_datetime)
    vfl.write(details)

setup(
  name = 'medharover',
  version=version,
  license='MIT',
  author="ConundrumArchives",
  author_email="nikhiltanni.githubemail@github.com",
  packages=find_packages('src', exclude="tests"),
  package_data={'': ['src/medhaboard/version.txt']},
  package_dir={'': 'src'},
  url='https://conundrumarchives.org/medha',
  keywords='Conundrum Archives Medha'
)