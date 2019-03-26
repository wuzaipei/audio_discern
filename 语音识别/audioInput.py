# coding:utf-8
import time
import wave
import pyaudio
from pymouse import PyMouse
from audioDiscern import audio_discern

# 用Pyaudio库录制音频
#   out_file:输出音频文件名
#   rec_time:音频录制时间(秒)
def audio_record(out_file, rec_time):
    CHUNK = 1024
    FORMAT = pyaudio.paInt16 #16bit编码格式
    CHANNELS = 1 #单声道
    RATE = 16000 #16000采样频率
    p = pyaudio.PyAudio()
    # 创建音频流
    stream = p.open(format=FORMAT, # 音频流wav格式
                    channels=CHANNELS, # 单声道
                    rate=RATE, # 采样率16000
                    input=True,
                    frames_per_buffer=CHUNK)
    print("Start Recording...")
    frames = [] # 录制的音频流
    # 录制音频数据
    for i in range(0, int(RATE / CHUNK * rec_time)):
        data = stream.read(CHUNK)
        frames.append(data)
    # 录制完成
    print(frames)
    stream.stop_stream()
    stream.close()
    p.terminate()
    print("Recording Done...")
    # 保存音频文件
    with wave.open(out_file, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        # wf.close()

# 控制鼠标滚动
def mouse_control(dir_tr):
    MOVE_DX = 5 # 每次滚动行数
    ms = PyMouse()
    horizontal = 0
    vertical = 0
    if dir_tr.find("上") != -1: # 向上移动
        vertical = MOVE_DX
        #print("vertical={0}, 向上".format(vertical))
    elif dir_tr.find("下") != -1: # 向下移动
        vertical = 0 - MOVE_DX
        #print("vertical={0}, 向下".format(vertical))
    elif dir_tr.find("左") != -1: # 向左移动
        horizontal = 0 - MOVE_DX
        #print("horizontal={0}, 向左".format(horizontal))
    elif dir_tr.find("右") != -1: # 向右移动
        horizontal = MOVE_DX
        #print("horizontal={0}, 向右".format(horizontal))
    #print("horizontal, vertical=[{0},{1}]".format(horizontal, vertical))
    # 通过scroll(vertical, horizontal)函数控制页面滚动
    # 另外PyMouse还支持模拟move光标,模拟鼠标click,模拟键盘击键等
    ms.scroll(vertical, horizontal)

while(True):
    # 请说出语音指令，例如["向上", "向下", "向左", "向右"]
    print("\n==================================================")
    print("请告诉我命令(限制在3秒内):")
    #print("Please tell me what you want to identify(limit within 10 seconds):")

    audio_path = "./audio/test1.wav"
    audio_type = "wav"
    audio_record(audio_path, 3) # 录制语音指令

    print("开始做语音识别...")
    asr_result =  audio_discern(audio_path,audio_type) # 识别语音指令
    print(asr_result)
    if asr_result["err_no"] == 0: # 语音识别结果不为空，识别结果为一个list
        text = asr_result["result"][0]
        mouse_control(text) # 根据识别结果控制页面滚动
        print("控制结束")
        if text.find("退出") != -1: # 如果是"退出"指令则结束程序
            break
        time.sleep(2) # 延时1秒

