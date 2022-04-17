import os
from time import sleep
from Utils.ProgressBar import ProgressBar1
from Utils.LogModule import init_logger
from Utils.FileUtils import rmdir, zipfolder, add_file_to_zip

# initialize logger
log = init_logger()

# update the steps when you add new step in execution below
totalsteps = 4

# initialize progressbar
pbar = ProgressBar1(totalsteps=totalsteps)

dist_dir = os.path.join("dist")
parent_dir = os.path.dirname(os.getcwd())

# clean create dist folder

# 1-clean dist folder
description = "Clean dist folder"
pbar.update(description=description)
sleep(1)

if (os.path.exists(dist_dir)):
  rmdir(dist_dir)

# 2-create dist folder
description = "Creating {ddir} folder".format(ddir=dist_dir)
pbar.update(description=description)

os.makedirs(dist_dir, exist_ok=True)
sleep(1)

# create distributions

# 3-create zip for Medha Board
description = "Packaging Medha Board"
pbar.update(description=description)
sleep(1)

zipname = os.path.join(dist_dir, "MedhaBoard")

zipfolder(zipname=zipname, target_dir=os.path.join(parent_dir, "MedhaBoard", "src"))

add_file_to_zip(zipname=zipname, targetfilepath=os.path.join(parent_dir, "requirements", "requirements_board_dep.txt"))

# 4-create zip for MedhaApplication
description = "Packaging Medha Applications"
pbar.update(description=description)
sleep(1)

zipname = os.path.join(dist_dir, "MedhaApplications")

zipfolder(zipname=zipname, target_dir=os.path.join(parent_dir, "MedhaApplication", "pythonImpl"))


pbar.done()