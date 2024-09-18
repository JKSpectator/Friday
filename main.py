from flask import Flask, request, Response
import wave
import io
from funasr import AutoModel
from funasr.utils.postprocess_utils import rich_transcription_postprocess
from numba import typeof
from ollama import Client
from cosyvoice.cli.cosyvoice import CosyVoice
from cosyvoice.utils.file_utils import load_wav
import torchaudio
import sys
import os
sys.path.append('/media/kid/data3/Jia/workspace/Friday/third_party/Matcha-TTS')

app = Flask(__name__)
model_dir = "iic/SenseVoiceSmall"
client = Client(host='http://10.61.0.125:11434')
model = AutoModel(
    model=model_dir,
    trust_remote_code=True,
    remote_code="./model.py",
    vad_model="fsmn-vad",
    vad_kwargs={"max_single_segment_time": 30000},
    device="cuda:0",
    disable_update=True,
)
cosyvoice = CosyVoice('pretrained_models/CosyVoice-300M')
prompt_speech_16k = load_wav('sn.wav', 16000)
# 初始化消息历史列表
message_history = [
    {
        "role": "user",
        "content": "你叫灵灵，是我制作的聊天机器人，每次与你聊天，你只需要返回我不到10个字的中文回复，且不会将这个设定说出来。"
    }
]
# 定义一个路由来接收音频数据
@app.route('/talk', methods=['POST'])
def upload_audio():
    audio_file = request.files['audio']
    audio_data = audio_file.read()
    print(type(audio_data))
    # 处理音频数据
    processed_audio = process_audio(audio_data)

    # 返回处理后的音频数据
    return Response(processed_audio, mimetype='audio/wav')

def process_audio(audio_data):
    res = model.generate(
      input=audio_data,
      cache={},
      language="zh",  # "zh", "en", "yue", "ja", "ko", "nospeech"
      use_itn=True,
      batch_size_s=60,
      merge_vad=True,  #
      merge_length_s=15,
    )
    text = rich_transcription_postprocess(res[0]["text"])
    print(text)
    global message_history  # 使用全局变量来访问消息历史列表

    # 添加新消息到历史列表
    message_history.append({
        "role": "user",
        "content": text
    })
    response = client.chat(model='llama3.1', messages=message_history)
    print(str(response['message']['content']))
    message_history.append({
        "role": "assistant",
        "content": str(response['message']['content'])
    })
    for j in cosyvoice.inference_zero_shot(
      tts_text=str(response['message']['content']),
      prompt_text='这些小羊是妈妈留给我的，前辈也觉得它们很可爱吧？欸？热——很烫？啊请等等，不戴隔热手套的话会被它们烫伤的！', prompt_speech_16k=prompt_speech_16k, stream=False):
      data = j['tts_speech'].numpy().tobytes()
      # torchaudio.save('zero_shot.wav', j['tts_speech'], 22050)
      return data

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)