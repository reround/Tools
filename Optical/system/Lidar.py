from ..basic.basic import *

import numpy as np
import matplotlib.pyplot as plt


class Lidar:
    def __init__(self, lambda_=1550e-9, pt=60e-3, gt=1.0, d=1.0, eta_sys=1.0, ka=1.0):
        """激光雷达

        Args:
            lambda_ (_type_, optional): 波长 - m. Defaults to 1550e-9.
            pt (_type_, optional): 发射激光功率 - W. Defaults to 60e-3.
            gt (float, optional): 发射天线增益 - dB. Defaults to 1.0.
            d (float, optional): 接受孔径 - m. Defaults to 1.0.
            eta_sys (float, optional): 激光雷达的光学系统的传输系数. Defaults to 1.0.
            ka (float, optional): 孔径透光常数. Defaults to 1.0.
        """
        self.lambda_ = lambda_
        self.pt = pt
        self.gt = gt
        self.d = d
        self.ka = ka

        self.eta_sys = eta_sys
        ...

    def get_Ar(self):
        return np.pi * np.power(self.d, 2)  # 有效接收面积

    def get_theta_t(self):
        # 发射激光的束宽
        return self.ka * self.lambda_ / self.d

    def action_distance_equation(self, r, sigma=1, eta_atm=1):
        """作用距离方程

        Args:
            r (_type_): 距离
            sigma (_type_): 目标的散射截面
            eta_atm (_type_): 单程大气传输系数

        Returns:
            _type_: 接收激光功率
        """
        num1 = self.pt * sigma * self.d**4 * eta_atm * self.eta_sys
        num2 = 16 * self.lambda_**2 * self.ka**2 * r**4
        print(num2)
        return num1 / num2


class Target:
    def __init__(self, Omega=1.0, dA=1.0, rho_t=0.8):
        """_summary_

        Args:
            Omega (float, optional): 目标的散射立体角. Defaults to 1.0.
            dA (float, optional): 目标的面积. Defaults to 1.0.
            rho_t (float, optional): 目标的平均反射系数. Defaults to 0.8.
        """
        self.Omega = Omega
        self.dA = dA
        self.rho_t = rho_t

    def get_sigma(self):
        return 4 * np.pi * self.rho_t * self.dA / self.Omega

