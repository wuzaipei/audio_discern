from aip import AipSpeech

def audio_discern(audio_path = "./audio/test.wav",audio_type = "wav"):

    """ 你的 APPID AK SK """
    APP_ID = '15857495' #''你的 App ID'
    API_KEY = '8oNWudGhOexb09KW8X2M2YLX' #'你的 Api Key'
    SECRET_KEY = 'F79btl1tnxfG4R8nMqRIRRAYdGznkfhH' #'你的 Secret Key'

    client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)

    # 读取文件
    def get_file_content(filePath):
        with open(filePath, 'rb') as fp:
            return fp.read()
    # 识别本地文件
    text = client.asr(get_file_content(audio_path), audio_type, 16000, {'dev_pid': 1536,})
    return text

