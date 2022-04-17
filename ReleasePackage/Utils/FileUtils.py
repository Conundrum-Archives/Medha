import os
from pathlib import Path
import zipfile

def rmdir(directory):
  directory = Path(directory)
  for item in directory.iterdir():
    if item.is_dir():
      rmdir(item)
    else:
      item.unlink()
  directory.rmdir()

  

def zipfolder(zipname, target_dir):            
  zipobj = zipfile.ZipFile(zipname + '.zip', 'w', zipfile.ZIP_DEFLATED)
  rootlen = len(target_dir) + 1
  for base, dirs, files in os.walk(target_dir):
    for file in files:
      fn = os.path.join(base, file)
      zipobj.write(fn, fn[rootlen:])
  zipobj.close()

def add_file_to_zip(zipname, targetfilepath):
  zipobj = zipfile.ZipFile(zipname + ".zip", "a", zipfile.ZIP_DEFLATED)
  zipobj.write(targetfilepath, os.path.basename(targetfilepath))
  zipobj.close()