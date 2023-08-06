"""
Extra functions that are not in the paper. Mostly my own experiments.
"""

import numpy as np
from pyPeriod import Periods

def stretch_by_time(periods, powers, bases, sr=1000, time=1, return_inverse=False):
  """
  Stretch by time. Give a samplerate (sr) and a time in seconds to stretch.
  This is accomplished by calculating the new duration in samples, then
  adding extra periods in each base until the new duration is attained.

  If return_inverse is true, the quasi-inverted periodicity transform is returned.
  Otherwise, the newly extended bases are returned. All other values are the same.
  """
  pass

def stretch_by_samples(periods, powers, bases, samples=0, return_inverse=False):
  """
  Stretch by samples. Give a number of samples to stretch by.
  This is accomplished by calculating the new duration in samples, then
  adding extra periods in each base until the new duration is attained.

  If return_inverse is true, the quasi-inverted periodicity transform is returned.
  Otherwise, the newly extended bases are returned. All other values are the same.
  """
  pass

def stretch_by_chunk(x, proportion=1, chunk_size=1024, overlap=0.5, algorithm='small_2_large'):
  """
  A way (???) to stretch a file incrementally.

  "Chunks" of the file are taken to be windows (a la FFT). They are then stretched by the
  proportion incrementally in one chunk at a time. Who knows if this will work.
  """
  pass
