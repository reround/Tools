"""
各种波形
"""

import numpy as np
import matplotlib.pyplot as plt


def sawtooth_wave(duration=1.0, num_samples=1000, amplitude=1.0, frequency=1.0):
    """生成锯齿波信号

    Args:
        duration (float, optional): 时长（周期数）. Defaults to 1.0.
        num_samples (int, optional): 采样点数. Defaults to 1000.
        amplitude (float, optional): 幅度. Defaults to 1.0.
        frequency (float, optional): 频率. Defaults to 1.0.
    """
    x = np.linspace(0, duration, num_samples)
    y = amplitude * (x % (1 / frequency)) * frequency * 2 - amplitude
    return x, y

    
if __name__ == "__main__":

    x, y = sawtooth_wave()
    # # 绘制锯齿波信号图像
    # print("x")
    plt.plot(x, y)
    # plt.xlabel("Time")
    # plt.ylabel("Amplitude")
    # plt.title("Sawtooth Waveform")
    # plt.grid(True)
    plt.show()
