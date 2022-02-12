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
with open(os.path.join("src", "medhalib", "version.txt"), "w") as vfl:
    details = str("""Version: {version} [Date: {date}]""").format(version=version, date=build_datetime)
    vfl.write(details)

setup(
  name = 'medhalib',
  version=version,
  license='MIT',
  author="ConundrumArchives",
  author_email="team@conundrumarchives.space",
  packages=find_packages('src', exclude="tests"),
  package_dir={'': 'src'},
  data_files=[
    ('', ["src/medhalib/version.txt"])
  ],
  include_package_data=True,
  tests_require = [
    "pytest"
  ],
  test_suite="tests",
  url='https://conundrumarchives.org/medha',
  keywords='Conundrum Archives Medha'
)
