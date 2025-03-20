import numpy as np

# Waveform Class
DEFAULT_BASELINE_BINS = np.arange(-49.5, 299.5,1)

DEFAULT_BASELINE_P0   = [100,0,20]

DEFAULT_SMOOTH_SIGMA  = 2

DEFAULT_WIDTH         = 6

DEFAULT_DISTANCE      = 10

DEFAULT_PROMINENCE    = 12

# Thresholds
PEAK_THRESH    = 125 #mV
INGRESS_THRESH = 50 #mV

# Region Of Interest
ROI_t_runs  = [-60, 50]
ROI_t_calib = [2, 85]