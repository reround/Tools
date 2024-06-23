# from const import *
from ..basic.basic import *

import numpy as np
import matplotlib.pyplot as plt


class Radar:
    def __init__(
        self,
        lambda_=1550e-9,
        Pt=1500,
        tau=2e-3,
        fr=10,
        T0=290,
        Gt=20,
        Gr=20,
        nf=7,
        loss=15,
        SNR_o=15,
    ):
        """雷达

        Args:
            lambda_ (_type_, optional): 脉冲宽度. Defaults to 1550e-9.
            Pt (_type_, optional): 发射峰值功率. Defaults to 60e-3.
            tau (_type_, optional): 脉冲宽度. Defaults to 1e-3.
            fr (_type_, optional): PRF. Defaults to 1e-3.
            T0 (int, optional): 温度 K. Defaults to 290.
            Gt (int, optional): 发射天线增益. Defaults to 1.
            Gr (int, optional): 接收天线增益. Defaults to 1.
            nf (float, optional): 系统噪声系数. Defaults to 0.3.
            loss (float, optional): 整个系统的损耗. Defaults to 0.3.
            SNR_o (int, optional): 探测所需的最小 SNR. Defaults to 1.
        """
        self.lambda_ = lambda_
        self.Pt = Pt
        self.tau = tau
        self.fr = fr
        self.T0 = T0
        self.Gt = Gt
        self.Gr = Gr
        self.nf = nf
        self.loss = loss
        self.SNR_o = SNR_o

        self.freq = c / self.lambda_
        self.pcw = self.Pt * self.tau * self.fr  # 平均连续波功率P

    def range_calc(self, range_=250e3, time_ti=10, sigma=10, radar_type=1, out_option=0):
        """计算 SNR 随时间的变化

        Args:
            te (_type_): _description_
            range_ (_type_): 距离
            time_ti (int, optional): 驻留间隔. Defaults to 10.
            sigma (int, optional): 目标截面积. Defaults to 1.
            radar_type (int, optional): _description_. Defaults to 1.
            out_option (int, optional): _description_. Defaults to 0.

        Returns:
            _type_: _description_
        """
        if radar_type == 0:
            pav = self.pcw
        else:
            # compute the duty cycle
            dt = self.tau * 1e-3 * self.fr
            pav = self.Pt * dt

        pav_db = to_dB(pav)
        lambda_sqdb = to_dB(np.power(self.lambda_, 2))
        sigma_db = to_dB(sigma)
        for_pi_cub = to_dB(np.power(4.0 * np.pi, 3))
        k_db = to_dB(k)
        te_db = to_dB(self.T0)
        ti_db = to_dB(time_ti)
        range_db = to_dB(range_)
        
        if out_option == 0:
            # compute SNR
            snr_out = (
                pav_db
                + self.Gt
                + self.Gr
                + lambda_sqdb
                + sigma_db
                + ti_db
                - for_pi_cub
                - k_db
                - te_db
                - self.nf
                - self.loss
                - 4.0 * range_db
            )
            index = 0
            snr = np.zeros(len(np.arange(10, 1000, 10)))
            for range_var in np.arange(10, 1000, 10):
                range_var_db = to_dB(range_var * 1000.0)
                snr[index] = (
                    pav_db
                    + self.Gt
                    + self.Gr
                    + lambda_sqdb
                    + sigma_db
                    + ti_db
                    - for_pi_cub
                    - k_db
                    - te_db
                    - self.nf
                    - self.loss
                    - 4.0 * range_var_db
                )
            var = np.arange(10, 1000, 10)
            print(len(snr))
            plt.scatter(var, snr)
            plt.xlabel("Range in Km")
            plt.ylabel("SNR in dB")
            plt.grid()
            plt.show()

        else:
            range4 = (
                pav_db
                + self.Gt
                + self.Gr
                + lambda_sqdb
                + sigma_db
                + ti_db
                - for_pi_cub
                - k_db
                - te_db
                - self.nf
                - self.loss
                - self.SNR_o
            )
            range_ = np.power(10.0, range4 / 40.0) / 100.0
            index = 0
            range_l = np.zeros(len(np.arange(10, 1000, 10)))
            for snr_var in np.arange(-20, 60, 1):
                rangedb = (
                    pav_db
                    + self.Gt
                    + self.Gr
                    + lambda_sqdb
                    + sigma_db
                    + ti_db
                    - for_pi_cub
                    - k_db
                    - te_db
                    - self.nf
                    - self.loss
                    - snr_var
                )
                range_l[index] = np.power(10.0, rangedb / 40.0) / 1000.0
            var = np.arange(-20, 60, 1)
            plt.plot(var, range_)
            plt.xlabel("Minimum SNR required for detection in dB")
            plt.ylabel("Maximum detection range in Km")
            plt.grid()
            plt.show()
        return 1
