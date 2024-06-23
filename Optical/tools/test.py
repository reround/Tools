# 设计切比雪夫II型滤波器
fp = 500  # 滤波器通带频率
fs1 = 750  # 滤波器阻带频率
sr2 = sr / 2  # 采样频率半周期每样本
Wp = fp / sr2  # 通带频率归一化
Ws = fs1 / sr2  # 阻带频率归一化
Rp = 3  # 通带最大损耗
Rs = 50  # 阻带最小衰减
n, Wn = signal.cheb2ord(
    Wp, Ws, Rp, Rs, analog=False, fs=None
)  # 当参数未归一化时，fs=sr
b, a = signal.cheby2(n, Rs, Wn, btype="lowpass", analog=False, output="ba", fs=None)
sos = signal.cheby2(n, Rs, Wn, btype="lowpass", analog=False, output="sos", fs=None)
w, h = signal.freqz(b, a, fs=sr)  # 返回的w单位与参数fs相同
plt.plot(w, 20 * np.log10(abs(h)))
plt.title("Chebyshev Type II frequency response")
plt.xlabel("Frequency [Hz]")
plt.ylabel("Amplitude [dB]")
plt.margins(0, 0.1)  # 去除画布四周白边
plt.grid(which="both", axis="both")  # 网格
plt.axvline(Wn * sr2, color="green")  # 绘制竖线，低通截止频率(取归一化)
plt.axhline(-Rs, color="green")  # 绘制横线，阻带衰减
plt.fill([fs1, fs1, sr2, sr2], [-Rs, 20, 20, -Rs], "0.9", lw=0)  # 阻带约束
plt.fill([0, 0, fp, fp], [-100, -Rp, -Rp, -100], "0.9", lw=0)  # 通带约束
plt.show()
