import sys
from pathlib import Path
import csv
import numpy as np
from scipy.optimize import curve_fit
from scipy.ndimage import gaussian_filter1d
from scipy.signal import find_peaks
import warnings

# Local modules
from utils.functions import gaussian

# Ignore warnings
warnings.filterwarnings("ignore")



""" ============= """
""" CONFIGURATION """
""" ============= """

DEFAULT_BASELINE_BINS = np.arange(-49.5, 299.5,1)

DEFAULT_BASELINE_P0   = [100,0,20]

DEFAULT_SMOOTH_SIGMA  = 2

DEFAULT_WIDTH         = 6

DEFAULT_DISTANCE      = 10

DEFAULT_PROMINENCE    = 12

""" ============ """


class Waveform:
    """
    <Description>
    """
    def __init__(self, csvfile):
        """
        <Description>

        Args:

        Returns:
        """
        self.csvfile            = csvfile
        self.raw_data           = None
        self.processed_data     = None
        self.baseline           = None
        self.main_peak_idx      = None
        self.ingress_idx        = None
        
        self.name               = self.csvfile.split("lcd")[1]

        # Read data from csv
        self.read_from_csv()


    """ ================== """
    """ Processing Methods """
    """ ================== """

    def read_from_csv(self):
        """
        <Description>

        Args:

        Returns:
        """
        try:
            with open(self.csvfile, 'r') as f:
                
                reader = csv.reader(f)
                
                try:
                    data   = np.array(list(reader), dtype=float)
                except ValueError:
                    pass
                    return # stops the function from running further
                
                try:
                    data   = data.T
                    data   = np.array(list(zip(data[0], data[1])))
    
                    self.raw_data       = data
                    self.processed_data = data
                    
                except Exception as e:
                    print(e)
            
        except FileNotFoundError:
            pass
        
        except PermissionError:
            pass
        
        except OSError:
            pass
            
        except Exception as e:
            pass


    def rescale(self, xfactor=1, yfactor=1):
        """
        <Description>

        Args:

        Returns:
        """
        # Get the processed data to rescale
        processed_data = self.get_data(zipped=True, raw=False)
        
        # Apply rescaling
        rescaled_data  = [(x * xfactor, y * yfactor) for x, y in processed_data]
        
        # Update
        self.processed_data = rescaled_data


    def calculate_baseline(self, 
                           bins = DEFAULT_BASELINE_BINS, 
                           p0   = DEFAULT_BASELINE_P0,
                           verbose = False):
        """
        <Description>

        Args:

        Returns:
        """
        # Extract waveform y-axis data
        _, y = self.get_data(zipped=False)

        # Generate numpy histogram
        hist, bin_edges = np.histogram(y, bins)

        # Get mid-points of bin edges so as to make x and y arrays plottable
        bin_mids = bin_edges[:-1] + np.diff(bin_edges)/2

        # Catch all zero indices
        zero_indexes = []
        for idx, y_val in enumerate(hist):
            if y_val == 0:
                zero_indexes.append(idx)

        # Remove zeros
        hist = np.delete(hist, zero_indexes, axis=None)
        bin_mids = np.delete(bin_mids, zero_indexes, axis=None)
        
        #plt.plot(bin_mids, hist)
        #plt.show()


        # Fit to Gaussian
        try:
            popt, pcov = curve_fit(gaussian, bin_mids, hist, p0=p0)
            baseline = popt[1] # the mean value of the fitted gaussian
            self.baseline = baseline
        except ValueError:
            print("ValueError")
        except RuntimeError:
            self.baseline = 0
            print("RuntimeError")
        except Exception as e:
            print(e)

        if verbose == True:
            return bin_mids, hist



    def zero_baseline(self):
        """
        <Description>

        Args:

        Returns:
        """
        baseline = self.get_baseline()

        data = self.get_data()
        baseline_corrected_data = [(x, y-baseline) for x,y in data]

        self.processed_data = baseline_corrected_data
        
        # Recalculate baseline for comparison
        self.calculate_baseline()


    def smooth(self, sigma=DEFAULT_SMOOTH_SIGMA):
        """
        <Description>

        Args:

        Returns:
        """
        x,y       = self.get_data(zipped=False)
        wf_smooth = gaussian_filter1d(y, sigma=sigma)

        smoothed_data = np.array(list(zip(x, wf_smooth)))
        self.processed_data = smoothed_data
        

    def detect_main_peak(self,
                         ROI, 
                         height, 
                         width      = DEFAULT_WIDTH, 
                         distance   = DEFAULT_DISTANCE, 
                         prominence = DEFAULT_PROMINENCE):
        """
        <Description>

        Args:
            ROI (tuple[int,int]) : integer value of the left-most and right-most INDEX of the
                                   Region Of Interest.

        Returns:
        """
        a = int(ROI[0]); b = int(ROI[1])
        _,y = self.get_data(zipped=False)
        wf_cut = y[a:b]

        # Find peaks
        try:
            peaks, _ = find_peaks(wf_cut, 
                                  height     = height, 
                                  width      = width, 
                                  distance   = distance, 
                                  prominence = prominence)

        except Exception as e:
            print(e)

        if len(peaks) > 0:
            try:
                # Extract index of first peak
                peak_idx = a + peaks[0]
                self.main_peak_idx = peak_idx
                return 1 # successfully found peaks
            except Exception as e:
                pass
        else:
            return 0 # no peaks detected


    def identify_ingress(self, threshold, ROI):
        """
        <Description>

        Args:

        Returns:
        """
        a = int(ROI[0])
        peak_idx, peak_val = self.get_main_peak()

        if peak_idx != None:
            _, y   = self.get_data(zipped=False)
            wf_cut = y[a:peak_idx]

            ingress_idx = a + np.argwhere(wf_cut >= threshold)[0][0]
            self.ingress_idx = ingress_idx
            return 1
        else:
            return 0            


    """ =========== """
    """ Get Methods """
    """ =========== """

    def get_data(self, zipped=True, raw=False):
        """
        <Description>

        Args:

        Returns:

        """
        if zipped == True:
            if raw == False:
                return self.processed_data
            else:
                return self.raw_data

        else:
            if raw == False:
                x,y = zip(*self.processed_data)
            else:
                x,y = zip(*self.raw_data)
            return np.array(x),np.array(y)


    def get_baseline(self):
        """
        <Description>

        Args:

        Returns:
        """
        return self.baseline


    def get_main_peak(self):
        """
        <Description>

        Args:

        Returns:
        """
        peak_idx = self.main_peak_idx

        if peak_idx != None:
            x, y = self.get_data(zipped=False)
            peak_val = y[peak_idx]

        else:
            peak_val = None

        return peak_idx, peak_val


    def get_ingress(self):
        """
        <Description>

        Args:

        Returns:

        """
        ingress_idx = self.ingress_idx

        if ingress_idx != None:
            x, _ = self.get_data(zipped=False)
            ingress_time_val = x[ingress_idx]

            return ingress_idx, ingress_time_val
        else:
            return None