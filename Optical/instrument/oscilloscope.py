#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   particular.py
@Time    :   2023/06/27 09:48
@Author  :   shun
@Description  :   特定的一些类
"""


import numpy as np
import matplotlib.pyplot as plt
from scipy import fftpack


class Oscilloscope:
    """示波器基类"""

    def __init__(self):
        pass

    def read_parameters(self) -> dict:
        """
        读取文件设置

        :return dict: 参数和值对应的字典
        """
        pass

    def read_data(self) -> tuple:
        """
        读取文件数据

        :return tuple: 返回两个列表，需要两个变量接收
        """
        pass


class Tek(Oscilloscope):
    """
    Tek 示波器文件类
    """

    def __init__(self, filename) -> int:
        self.filename = filename
        self.parameters = self.read_parameters()
        self.t, self.s = self.read_data()

        self.Record_Length = (
            self.parameters["Record Length"].astype(np.float64).astype(np.int64)
        )
        self.Sample_Interval = self.parameters["Sample Interval"].astype(np.float64)
        self.Trigger_Point = self.parameters["Trigger Point"].astype(np.float64)
        self.Source = self.parameters["Source"]
        self.Vertical_Units = self.parameters["Vertical Units"]
        self.Vertical_Scale = self.parameters["Vertical Scale"].astype(np.float64)
        self.Vertical_Offset = self.parameters["Vertical Offset"].astype(np.float64)
        self.Horizontal_Units = self.parameters["Horizontal Units"]
        self.Horizontal_Scale = self.parameters["Horizontal Scale"].astype(np.float64)
        self.Pt_Fmt = self.parameters["Pt Fmt"]
        self.Yzero = self.parameters["Yzero"].astype(np.float64)
        self.Probe_Atten = self.parameters["Probe Atten"].astype(np.float64)
        self.Model_Number = self.parameters["Model Number"]
        self.Serial_Number = self.parameters["Serial Number"].astype(np.float64)
        self.Firmware_Version = self.parameters["Firmware Version"]

        self.total_time = self.Sample_Interval * self.Record_Length
        self.Sample_Rate = 1 / self.Sample_Interval

    def read_parameters(self) -> dict:
        """
        读取 tex 文件设置

        :return dict: 参数和值对应的字典
        """
        data = np.loadtxt(
            self.filename, dtype="str", delimiter=",", usecols=(0, 1), unpack=True
        )
        temp = {
            key: value for key, value in zip(data[0][:18], data[1][:18]) if key != ""
        }
        return temp

    def read_data(self) -> tuple:
        """
        读取 tex 文件数据

        :return tuple: 返回第3、4列，两个列表，需要两个变量接收
        """
        data = np.loadtxt(self.filename, delimiter=",", usecols=(3, 4), unpack=True)
        return (data[0], data[1])

    def time_domain(self, start=0, end=-1):
        """绘制信号时域图

        Args:
            start (int, optional): 起始点. Defaults to 0.
            end (int, optional): 终止点. Defaults to -1.
        """
        # 时域
        x = np.linspace(0, self.total_time, self.Record_Length)
        plt.plot(x[start:end], self.s[start:end])
        plt.title(
            "Time domain: "
            + "\n"
            + self.filename
            + "\n"
            + str(self.total_time)
            + str(self.Horizontal_Units)
        )
        plt.xlabel("Time (s)")
        plt.ylabel("Amplitude")
        plt.show()

    def spectrum_domain(self, isdB=False):
        if isdB:
            s_fft = 10 * np.log10(fftpack.fft(self.s))
            f = fftpack.fftfreq(self.Record_Length, self.Sample_Interval)
        else:
            # 频域
            s_fft = fftpack.fft(self.s)
            f = fftpack.fftfreq(self.Record_Length, self.Sample_Interval)
        mask = f > 0
        plt.plot(f[mask], abs(s_fft[mask]))
        plt.title("Frequency Spectrum: " + "\n" + self.filename)
        plt.xlabel("Frequency (Hz)")
        plt.ylabel("Amplitude")
        plt.show()


class UntitleOs(Oscilloscope):
    def __init__(self, filename: str):
        self.filename = filename
        self.parameters = self.read_parameters()
        self.t, self.s = self.read_data()

        self.Record_Length = self.parameters['"Record Length"'].astype(np.int64)
        self.Sample_Interval = self.parameters['"Sample Interval"'].astype(np.float64)
        self.Trigger_Point = self.parameters['"Trigger Point"'].astype(np.int64)
        self.Trigger_Time = self.parameters['"Trigger Time"'].astype(np.float64)
        self.Horizontal_Offset = self.parameters['"Horizontal Offset"'].astype(
            np.float64
        )

        self.total_time = self.Sample_Interval * self.Record_Length
        self.Sample_Rate = 1 / self.Sample_Interval

    def read_parameters(self) -> dict:
        """
        读取文件设置

        :return dict: 参数和值对应的字典
        """
        data = np.loadtxt(
            self.filename, dtype="str", delimiter=",", usecols=(0, 1), unpack=True
        )
        temp = {key: value for key, value in zip(data[0][:6], data[1][:6]) if key != ""}
        return temp

    def read_data(self) -> tuple:
        """
        读取 tex 文件数据

        :return tuple: 返回第3、4列，两个列表，需要两个变量接收
        """
        data = np.loadtxt(self.filename, delimiter=",", usecols=(3, 4), unpack=True)
        return (data[0], data[1])


if __name__ == "__main__":
    pass
