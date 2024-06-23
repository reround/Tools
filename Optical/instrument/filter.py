import numpy as np  
from scipy.signal import butter, lfilter  
  
def lowpass_filter(signal, fs, cutoff, order=6):  
    """  
    对信号应用低通滤波器。  
  
    参数:  
        signal (np.ndarray): 输入信号  
        fs (float): 采样频率（Hz）  
        cutoff (float): 截止频率（Hz）  
        order (int, 可选): 滤波器阶数，默认为6  
  
    返回:  
        np.ndarray: 滤波后的信号  
    """  
    # 归一化截止频率  
    Wn = cutoff / (0.5 * fs)  
  
    # 设计巴特沃斯滤波器  
    b, a = butter(N=order, Wn=Wn, btype='low')  
  
    # 应用滤波器  
    filtered_signal = lfilter(b, a, signal)  
  
    return filtered_signal  

if __name__ == '__main__':
    # 示例使用  
    # 采样频率和信号参数  
    fs = 1000  # 采样频率 Hz  
    t = np.arange(0, 1.0, 1/fs)  # 时间向量  
    f = 50  # 信号频率 Hz  
    
    # 创建一个包含50Hz正弦波和250Hz正弦波的信号  
    x = 0.7*np.sin(2*np.pi*f*t) + 0.5*np.sin(2*np.pi*5*f*t)  
    
    # 应用低通滤波器  
    y = lowpass_filter(x, fs, 60)  
    
    # 绘制原始信号和滤波后的信号  
    import matplotlib.pyplot as plt  
    plt.figure()  
    plt.plot(t, x, label='Original signal')  
    plt.plot(t, y, label='Filtered signal')  
    plt.xlabel('Time [s]')  
    plt.ylabel('Amplitude')  
    plt.legend()  
    plt.grid(True)  
    plt.show()