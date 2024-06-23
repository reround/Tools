from const import *
from DrawStyle import *

import numpy as np

def pulse_train(tau, pri, p_peak):
    """计算占空因子、平均发射功率、脉冲能量和脉冲重复频

    Args:
        tau (_type_): 脉冲宽度
        pri (_type_): PRI
        p_peak (_type_): 峰值功率

    Returns:
        _type_: dt 占空因子, pav 平均发射功率, ep 脉冲能量, prf PRF, ru 非模糊距离(km)
    """
    return dt, pav, ep, prf, ru

