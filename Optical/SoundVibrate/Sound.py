import matplotlib.pyplot as plt
import matplotlib as mpl
import wave
import pyaudio
import numpy as np


class Sound:
    def __init__(
        self,
        rate: int = 44100,
        chunk: int = 1024,
        format_=pyaudio.paInt16,
        channal: int = 1,
    ):
        """声音

        Args:
            rate (int, optional): 采样速率. Defaults to 44100.
            chunk (int, optional): 块大小. Defaults to 1024.
            format_ (_type_, optional): 格式. Defaults to pyaudio.paInt16.
            channal (int, optional): 声道数. Defaults to 1.
        """
        self.p = pyaudio.PyAudio()
        self.rate = rate
        self.chunk = chunk
        self.format = format_
        self.channal = channal

    def open_stream(self, input_=False):
        """打开流

        Args:
            input_ (bool, optional): 是否能够写入. Defaults to False.
        """
        self.stream = self.p.open(
            format=self.format,
            channels=self.channal,
            rate=self.rate,
            output=True,
            input=input_,
        )

    def close_stream(self):
        """关闭流"""
        self.stream.stop_stream()
        self.stream.close()

    def creat_wav_with_ndarray(self, array: np.ndarray, filename: str):
        """从 np.ndarray 序列制作音频
        目前是整体处理，文件肯定不能特别大

        Args:
            array (np.ndarray): np.ndarray 序列
            filename (str): 音频文件名
        """
        array_bytes = array.astype(np.int16).tobytes()
        wf = wave.open(filename, "wb")
        wf.setnchannels(self.channal)
        wf.setsampwidth(self.p.get_sample_size(self.format))
        wf.setframerate(self.rate)
        wf.writeframes(array_bytes)
        wf.close()

    def play_ndarray(self, array: np.ndarray):
        """播放 np.ndarray 形式的音频
        目前是整体处理，文件肯定不能特别大

        Args:
            array (np.ndarray): np.ndarray 序列
        """
        # 防止声音过小
        array_max = np.max(array)
        if array_max < 5000:
            array *= 5000 / array_max
        array_bytes = array.astype(np.int16).tobytes()
        self.open_stream()
        self.stream.write(array_bytes)
        self.close_stream()
        self.p.terminate()

    def record(self, filename: str, record_seconds):
        """记录声音
        目前是整体处理，文件肯定不能特别大

        Args:
            filename (str): 保存的文件名
            record_seconds (_type_): 录音时间
        """
        frames = []
        self.open_stream(input_=True)

        print("Record start ...")
        for i in range(0, int(self.rate / self.chunk * record_seconds)):
            data = self.stream.read(self.chunk)
            frames.append(data)
        print("Record end.")
        self.close_stream()
        self.p.terminate()

        wf = wave.open(filename, "wb")
        wf.setnchannels(self.channal)
        wf.setsampwidth(self.p.get_sample_size(self.format))
        wf.setframerate(self.rate)
        wf.writeframes(b"".join(frames))
        wf.close()


if __name__ == "__main__":

    fs = 22050
    x = np.linspace(0, 3, 22050 * 3)
    b = np.sin(2 * np.pi * 440 * x) * 10000
    b = np.array(b)
    # b = np.array(b).astype(np.int16).tobytes()

    s = Sound(rate=fs)
    s.play_ndarray(b)
    # s.creat_wav_with_ndarray(b, "xx.wav")
    # s.record("hello.wav", 3)
