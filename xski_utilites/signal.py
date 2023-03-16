from scipy.signal import butter, filtfilt, resample
from scipy.interpolate import interp1d
from scipy.ndimage import gaussian_filter1d
import numpy as np
import pandas as pd

def low_pass_filter(sig, fs, f_cut, order):
    """
    applies zero-lag butterworth filter to a signal
    :param sig: signal to be filtered - np.array
    :param fs: sampling frequency of sig - integer
    :param f_cut: cut-off frequency (low-pass) - integer
    :param order: order of filter - integer
    :return sig_filt: filtered signal - np array
    """
    # design filter
    nf = f_cut/(fs/2)
    b, a = butter(order, nf, btype='low')

    # apply filter
    sig_filt = filtfilt(b, a, sig, axis=0, padtype='odd', padlen=3*(max(len(b), len(a))-1))
    return sig_filt

def downsample(input_data_df, original_sampling_rate_hz, target_sampling_rate_hz):
    """Downsample the data in the input_data_df from the original sampling rate to a given target sampling rate."""
    data_array = input_data_df.values
    len_data = data_array.shape[0]
    current_x = np.linspace(0, len_data, len_data)
    data_array_downsampled = interp1d(current_x, data_array, axis=0)(
        np.linspace(0, len_data, int(len_data * target_sampling_rate_hz / original_sampling_rate_hz))
    )

    output_data_df = pd.DataFrame(data_array_downsampled, columns=input_data_df.columns)

    return output_data_df

def resample_timeseries(ts, n_samples = 100):
    ts_resampled = resample(ts, n_samples)
    ts_smooth = gaussian_filter1d(ts_resampled, sigma = 4)
    return ts_smooth

def downsample(input_data_df, original_sampling_rate_hz, target_sampling_rate_hz):
    """Downsample the data in the input_data_df from the original sampling rate to a given target sampling rate."""
    data_array = input_data_df.values
    len_data = data_array.shape[0]
    current_x = np.linspace(0, len_data, len_data)
    data_array_downsampled = interp1d(current_x, data_array, axis=0)(
        np.linspace(0, len_data, int(len_data * target_sampling_rate_hz / original_sampling_rate_hz))
    )

    output_data_df = pd.DataFrame(data_array_downsampled, columns=input_data_df.columns)

    return output_data_df

def get_normalization_idx(array, output_length):
    """

    :param array: some array to be downsampled
    :param output_length: requested output length
    :return: list with idx for normalization
    """
    a = np.arange(len(array))
    anorm=(a-min(a))/(max(a)-min(a))*(output_length-1)
    idx_norm = [np.argmin(abs(x - anorm)) for x in np.arange(output_length)]

    return idx_norm

def find_projection_index(gps, long_p, lat_p):
    """
    finds the projection of a specific section point on the gps data of each participant
    :param gps: data frame containing 'Longitude' and 'Latitude' time series
    :param long_p: Longitude coordinate of requested point
    :param lat_p: Latitude coordinate of requested point
    :return: index where to find the projection
    """
    return np.argmin(np.sqrt((long_p-gps['Longitude'].values)**2 + (lat_p-gps['Latitude'].values)**2))+gps.index[0]

def low_pass_filter_series(sig, fs=100, f_cut=5, order=2):
    """
    ready for being used in a apply function
    applies zero-lag butterworth filter to a signal
    :param sig: signal to be filtered - series
    :param fs: sampling frequency of sig - integer
    :param f_cut: cut-off frequency (low-pass) - integer
    :param order: order of filter - integer
    :return sig_filt: filtered signal - np array
    """
    # design filter
    sig_array = sig.values
    nf = f_cut/(fs/2)
    b, a = butter(order, nf, btype='low')

    # apply filter
    sig_filt = filtfilt(b, a, sig_array, axis=0, padtype='odd', padlen=3*(max(len(b), len(a))-1))
    return pd.Series(sig_filt, name=sig.name)
