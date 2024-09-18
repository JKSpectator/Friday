import requests


def send_audio_to_server(url, audio_file_path):
    # 打开音频文件并读取数据
    with open(audio_file_path, 'rb') as audio_file:
        files = {'audio': (audio_file_path, audio_file, 'audio/wav')}
        print(files)

        # 发送POST请求到服务器
        response = requests.post(url, files=files)

        # 检查响应状态码
        if response.status_code == 200:
            print("Audio processed successfully")
            # 播放或保存服务器返回的音频数据
            # 这里只是简单地打印出响应的内容
            print(response.content)
        else:
            print("Error:", response.status_code, response.text)


# 服务器URL
server_url = 'http://127.0.0.1:5000/talk'

# 音频文件路径
audio_file_path = 'zero_shot_0.wav'

# 调用函数发送音频
send_audio_to_server(server_url, audio_file_path)