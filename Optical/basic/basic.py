import numpy as np

c = 299_792_458 # 光速
k = 1.38e-23 # 玻尔兹曼常数


def to_dB(x):
    """计算 dB

    Args:
        x (_type_): _description_

    Returns:
        _type_: _description_
    """
    return 10 * np.log10(x)


def from_dB(x):
    """计算比例 dB

    Args:
        x (_type_): _description_

    Returns:
        _type_: _description_
    """
    return np.power(10, (x / 10))


def loss(x, l):
    """计算衰减后的值

    Args:
        x (_type_): 输入值
        l (_type_): 衰减（dB）

    Returns:
        _type_: 输出值
    """
    return from_dB(l) * x
