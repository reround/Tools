import numpy as np
import matplotlib.pyplot as plt
from scipy import fftpack


def plot_fft(signal, length, sample_interval, isdB=False):
    """绘制 signal 的傅里叶变换

    Args:
        signal (_type_): _description_
        length (_type_): _description_
        sample_interval (_type_): _description_
        isdB (bool, optional): _description_. Defaults to False.
    """
    if isdB:
        s_fft = 10 * np.log10(fftpack.fft(signal))
        f = fftpack.fftfreq(length, sample_interval)
    else:
        # 频域
        s_fft = fftpack.fft(signal)
        f = fftpack.fftfreq(length, sample_interval)
    mask = f > 0
    plt.plot(f[mask], abs(s_fft[mask]))
    plt.title("Frequency Spectrum")
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Amplitude")
    plt.show()
