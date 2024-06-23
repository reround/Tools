import wave
import pyaudio
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl


# 按键中断: 按下按键执行该函数
def on_press(event):
    global stream, p, END
    if event.key == "q":
        stream.stop_stream()
        stream.close()
        p.terminate()
        plt.close()
        END = True


CHUNK = 1024 * 8
wf = wave.open("output.wav", "rb")
p = pyaudio.PyAudio()

stream = p.open(
    format=p.get_format_from_width(wf.getsampwidth()),
    channels=wf.getnchannels(),
    rate=wf.getframerate(),
    output=True,
)

data = wf.readframes(CHUNK)


# 作图的设置
mpl.rcParams["toolbar"] = "None"
fig, ax = plt.subplots(figsize=(12, 3))
fig.canvas.mpl_connect("key_press_event", on_press)
plt.subplots_adjust(left=0.001, top=0.999, right=0.999, bottom=0.001)
plt.get_current_fig_manager().set_window_title("Wave")
x = np.arange(0, CHUNK)
(line,) = ax.plot(x, np.random.rand(CHUNK), color="#C04851")
ax.set_xlim(0, CHUNK - 1)
ax.set_ylim(-(2**7), 2**7)
plt.axis("off")
plt.ion()
plt.show()


while data:
    try:
        stream.write(data)
    except OSError as e:
        if e.errno == -9988:
            # 处理流已关闭的情况
            print("Stream is closed.")
        else:
            # 处理其他类型的 OSError
            print(f"An OSError occurred: {e}")
    except Exception as e:
        # 处理其他类型的异常
        print(f"An exception occurred: {e}")

    # 绘图
    try:
        data = np.frombuffer(data, dtype=np.int16)
        line.set_ydata(data / 100)
        fig.canvas.draw()
        fig.canvas.flush_events()
    except ValueError as ve:
        print("wave end.")

    # 读取下一帧
    data = wf.readframes(CHUNK)


stream.stop_stream()
stream.close()
p.terminate()
wf.close()
