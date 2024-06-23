from const import *
from DrawStyle import *

import numpy as np


def radar_eq(pt, freq, g, sigma, b, nf, loss, range_):
    """_summary_

    Args:
        pt (_type_): 峰值功率
        freq (_type_): 雷达中心频率
        g (_type_): 天线增益
        sigma (_type_): 目标截面积
        b (_type_): 带宽
        nf (_type_): 噪声系数
        loss (_type_): 雷达损耗
        range (_type_): 目标距离(可以是一个单值或者一个向量)

    Returns:
        snr: SNR(单值或者向量，取决于目标距离)
    """
    range_ = np.array(range_)
    lambda_ = c / freq
    p_peak = 10 * np.log10(pt)
    lambda_sqdb = 10 * np.log10(lambda_**2)
    sigma_db = 10 * np.log10(sigma)
    four_pi_cub = 10 * np.log10((4.0 * np.pi) ** 3)
    k_db = 10 * np.log10(k)
    to_db = 10 * np.log10(290)
    b_db = 10 * np.log10(b)
    range_pwr4_db = 10 * np.log10(np.power(range_, 4))
    # print(range_pwr4_db)

    num = p_peak + g + g + lambda_sqdb + sigma_db
    den = four_pi_cub + k_db + to_db + b_db + nf + loss + range_pwr4_db
    # print(den)
    snr = num - den
    # print(snr)
    return snr


@ds_01
def diff_sigma():
    snr1 = radar_eq(
        1.5e6, 5.6e9, 45, 0.1 * 10, 5e6, 3, 6, range_=np.linspace(25e3, 165e3, 1000)
    )
    snr2 = radar_eq(
        1.5e6, 5.6e9, 45, 0.1, 5e6, 3, 6, range_=np.linspace(25e3, 165e3, 1000)
    )
    snr3 = radar_eq(
        1.5e6, 5.6e9, 45, 0.1 / 10, 5e6, 3, 6, range_=np.linspace(25e3, 165e3, 1000)
    )
    plt.plot(snr1, label="$\sigma$ = 0dbsm")
    plt.plot(snr2, label="$\sigma$ = -10dbsm")
    plt.plot(snr3, label="$\sigma$ = -20dbsm")
    plt.ylabel("SNR/dB")
    plt.xlabel("Distance /km")
    plt.legend()
    plt.show()


@ds_01
def diff_pt():
    snr1 = radar_eq(
        2.16e6, 5.6e9, 45, 0.1, 5e6, 3, 6, range_=np.linspace(25e3, 165e3, 1000)
    )
    snr2 = radar_eq(
        1.5e6, 5.6e9, 45, 0.1, 5e6, 3, 6, range_=np.linspace(25e3, 165e3, 1000)
    )
    snr3 = radar_eq(
        0.6e6, 5.6e9, 45, 0.1, 5e6, 3, 6, range_=np.linspace(25e3, 165e3, 1000)
    )
    plt.plot(snr1, label="$P_t$ = 2.16MW")
    plt.plot(snr2, label="$P_t$ = 1.5MW")
    plt.plot(snr3, label="$P_t$ = 0.6MW")
    plt.ylabel("SNR/dB")
    plt.xlabel("Distance /km")
    plt.legend()
    plt.show()


if __name__ == "__main__":
    diff_pt()
    diff_sigma()
