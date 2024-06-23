"""定义一些绘图的样式
"""

import matplotlib.pyplot as plt


def ds_01(func):
    def inner():

        plt.grid()
        plt.rcParams["font.family"] = "serif"
        plt.rcParams["font.serif"] = ["Times New Roman"]
        plt.rcParams["font.size"] = 15
        func()
        plt.rcParams.update(plt.rcParamsDefault)

    return inner
