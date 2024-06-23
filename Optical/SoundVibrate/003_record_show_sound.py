import pyaudio
import wave
import pyaudio  # 收集声音
import numpy as np  # 处理声音数据
import matplotlib.pyplot as plt  # 作图
import matplotlib as mpl


# 按键中断: 按下按键执行该函数
def on_press(event):
    global stream, p, END
    if event.key == "q":
        plt.close()
        stream.stop_stream()
        stream.close()
        p.terminate()
        END = True


CHUNK = 1024  # 录音块大小
FORMAT = pyaudio.paInt16  # 采样点16位
CHANNELS = 1  # 立体声
RATE = 44100  # 采样频率
RECORD_SECONDS = 5  # 录音时间
WAVE_OUTPUT_FILENAME = "output.wav"

p = pyaudio.PyAudio()
stream = p.open(
    format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK
)

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

print("开始录音...")

frames = []

for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    try:
        data = stream.read(CHUNK)
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

    frames.append(data)
    data = np.frombuffer(data, dtype=np.int16)

    line.set_ydata(data / 100)
    fig.canvas.draw()
    fig.canvas.flush_events()

print("录音结束...")

stream.stop_stream()
stream.close()
p.terminate()

wf = wave.open(WAVE_OUTPUT_FILENAME, "wb")
wf.setnchannels(CHANNELS)
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b"".join(frames))
wf.close()
