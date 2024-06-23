"""
信号调制
"""

import numpy as np
import matplotlib.pyplot as plt


def mapping(sig: np.ndarray, start, end) -> np.ndarray:
    """将 sig 的值范围映射到 (start, end) 范围

    Args:
        sig (np.ndarray): 一维序列
        start (_type_): 范围起点
        end (_type_): 范围终点

    Returns:
        np.ndarray: (start, end) 范围的信号
    """
    min_value = np.min(sig)
    max_value = np.max(sig)
    sig_m = np.interp(sig, (min_value, max_value), (start, end))
    return sig_m


def frequency_modulation(mod_sig: np.ndarray, sampling_rate: np.ndarray) -> np.ndarray:
    """频率调制

    Args:
        mod_sig (np.ndarray): 调频信号
        sampling_rate (np.ndarray): 载波信号

    Returns:
        np.ndarray: 调制信号
    """
    phase = 2 * np.pi * np.cumsum(mod_sig) / sampling_rate
    signal = np.sin(phase)
    return signal


def amplitude_modulation(mod_sig: np.ndarray, ori_sig: np.ndarray) -> np.ndarray: ...


def phase_modulation(mod_sig: np.ndarray, ori_sig: np.ndarray) -> np.ndarray: ...


if __name__ == "__main__":

    # 设置参数
    frequency_start = 100  # 起始频率
    frequency_end = 500  # 终止频率
    duration = 1.0  # 信号时长（秒）
    sampling_rate = 44100  # 采样率

    # 生成时间轴
    t = np.linspace(0, duration, int(sampling_rate * duration))

    # 生成频率随时间变化的信号
    frequency_signal = np.sin(2 * np.pi * t)  # 使用正弦信号代表频率变化

    freq = mapping(frequency_signal, frequency_start, frequency_end)
    signal = frequency_modulation(freq, sampling_rate)

    plt.plot(signal)
    # plt.xlabel("Time")
    # plt.ylabel("Amplitude")
    # plt.title("Sawtooth Waveform")
    # plt.grid(True)
    plt.show()
