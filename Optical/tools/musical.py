"""
音乐乐器波形
"""

import numpy as np
import wave
from numpy import pi
import math
import pyaudio
import matplotlib.pyplot as plt


# p = pyaudio.PyAudio()

sample_rate = 22050  # 采样率
sample_width = 2  # 位深
time = 1
arr = 0


# 波形生成
def wave_bulid(f0, amplitude_xishu=0.5, time=time):

    w_oumiga = 2 * pi * f0
    w_oumiga1 = 2 * pi * 100
    # 波形时间
    x = np.linspace(0, time, sample_rate * time)
    amplitude = math.pow(2, 8 * sample_width - 1) * amplitude_xishu  # 振幅
    y = amplitude * np.sin(w_oumiga * x)
    # y = amplitude*(np.sin(w_oumiga*x-pi)+np.sin(w_oumiga1*x-pi))
    return x, y, f0
    # [130.81, 138.59, 146.83, 155.56, 164.81, 174.61, 184.99, 195.99, 207.65, 220, 233.08, 246.94,
    #  261.62, 277.18, 293.67, 311.13, 329.63, 349.23, 369.99, 391.99, 415.31, 440, 466.16, 493.88,
    #  523.25, 554.36, 587.33, 622.25, 659.26, 698.46, 739.99, 783.99, 830.61, 880, 932.32, 987.76] # C3-B5，钢琴基频


def piano_():
    arr = 0
    for f0 in [261.62, 293.67, 329.63, 349.23, 391.99, 440, 493.88]:  # C4-B4，钢琴基频
        # 钢琴音频域多次谐波与基频比例关系
        Amp = [
            1,
            0.340,
            0.102,
            0.085,
            0.070,
            0.065,
            0.028,
            0.085,
            0.011,
            0.030,
            0.010,
            0.014,
            0.012,
            0.013,
            0.004,
            0.004,
            0.004,
            0.004,
            0.004,
            0.004,
        ]
        # m = int(5000/f0)
        n = len(Amp)  # 谐波个数
        # print(n)
        y = 0
        for i in range(0, n):
            xishu = 1 / 2 * Amp[i]
            # if f0*i >5000:
            #     print(i)
            #     break
            x, tempy, fn = wave_bulid(f0 * (i + 1), xishu)
            y += tempy

        # 幅值变化模型
        a = sample_rate * time
        attenuation = [0 for x in range(0, a)]
        for i in range(0, int(2 / 80 * a)):
            attenuation[i] = 0.2 + i * 0.8 / int(2 / 80 * a)
        for i in range(int(2 / 80 * a), int(8 / 80 * a)):
            attenuation[i] = 1 - (i - 2 / 80 * a) * 0.6 / (
                int(8 / 80 * a) - int(2 / 80 * a)
            )
        for i in range(int(8 / 80 * a), int(4 / 8 * a)):
            attenuation[i] = 0.4 - (i - int(8 / 80 * a)) * 0.2 / (
                int(4 / 8 * a) - int(8 / 80 * a)
            )
        for i in range(int(4 / 8 * a), int(8 / 8 * a)):
            # attenuation[i] = 0.2
            attenuation[i] = 0.2 - (i - int(4 / 8 * a)) * 0.1 / (
                int(8 / 8 * a) - int(4 / 8 * a)
            )

        # print(x,y)
        y *= attenuation
        arr = np.append(arr, y)
        zero = np.zeros(5500)  # 延迟
        arr = np.append(arr, zero)

    # 保存文
    # print(len(y),len(attenuation))
    y_data = arr.astype(np.int16).tobytes()  # 转字节
    return y_data


# wf = wave.open(r"piano1.wav", "wb")  # 保存文件地址
# wf.setnchannels(1)  # 声道设置
# wf.setsampwidth(2)  # 采样位数设置
# wf.setframerate(sample_rate)
# wf.writeframes(y_data)


def save_audio(
    file_name,
    audio,
    channels=1,
    rate=22050,
):
    """保存音频

    Args:
        file_name (_type_): 文件名
        audio (_type_): bytes 序列
        channels (int, optional): 通道数. Defaults to 1.
        rate (int, optional): 采样率. Defaults to 22050.
    """
    wf = wave.open(file_name, "wb")  # 保存文件地址
    wf.setnchannels(channels)  # 声道设置
    wf.setsampwidth(2)  # 采样位数设置
    wf.setframerate(rate)
    wf.writeframes(audio)


def play_audio(
    audio,
    channels=1,
    rate=22050,
    output=True,
    frames_per_buffer=1024,
):
    """ 播放音频

    Args:
        audio (_type_): bytes 序列
        channels (int, optional): 通道数. Defaults to 1.
        rate (int, optional): 采样率. Defaults to 22050.
        output (bool, optional): _description_. Defaults to True.
        frames_per_buffer (int, optional): _description_. Defaults to 1024.
    """
    p = pyaudio.PyAudio()
    stream = p.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=sample_rate,
        output=True,
        frames_per_buffer=1024,
    )
    stream.write(audio)
    stream.close()
    p.terminate()


if __name__ == "__main__":
    play_audio(piano_())
