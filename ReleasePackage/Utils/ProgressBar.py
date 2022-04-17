from itertools import count
from tqdm import tqdm

class ProgressBar1:

  def __init__(self, totalsteps=100):
    self.totalsteps = totalsteps
    self.progress_bar = tqdm(range(self.totalsteps))
    self.progress_bar.refresh()
    self.count = 0

  def update(self, description="", step=1, direction=1):
    if (step < 0 or step > self.totalsteps):
      print("ERROR: step value for update must be between 0 to total steps value ({tsteps})".format(tsteps=self.totalsteps))
      return

    self.count = self.count + (step * direction)
    self.progress_bar.update(self.count)
    self.progress_bar.set_description(description)
    self.progress_bar.refresh()

  def done(self):
    self.progress_bar.set_description("Done")
    self.progress_bar.close()