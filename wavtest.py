import wave

def get_wav_info(file_path):
    with wave.open(file_path, 'r') as wav_file:
        # 获取WAV文件的参数
        params = wav_file.getparams()
        channels = params.nchannels
        sample_width = params.sampwidth
        framerate = params.framerate
        nframes = params.nframes
        bits_per_sample = sample_width * 8  # 位深是字节宽度的8倍

        print(f"Channels: {channels}")
        print(f"Sample Width (bytes): {sample_width}")
        print(f"Frame Rate (samples per second): {framerate}")
        print(f"Total Frames: {nframes}")
        print(f"Bits Per Sample: {bits_per_sample}")

# 替换为你的WAV文件路径
file_path = 'zero_shot_0.wav'
get_wav_info(file_path)