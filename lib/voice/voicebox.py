# PythonからVOICEVOXを実行する

import requests
import json
import sounddevice as sd
import numpy as np
import os

class VoiceBox:
    def __init__(self, logger):
        self.host = "127.0.0.1"
        self.port = "50021"
        self.speaker = 3
        self.logger = logger
        self.logger.name = __name__


    def post_audio_query(self, text: str) -> dict:
        # 音声合成用のクエリを作成する
        params = {"text": text, "speaker": self.speaker}

        res = requests.post(
            f"http://{self.host}:{self.port}/audio_query",
            params=params,
        )

        query_data = res.json()
        query_data["speedScale"] = 1.5

        return query_data


    def post_synthesis(self, query_data: dict) -> bytes:
        # 音声合成を実行する
        params = {"speaker": self.speaker}
        headers = {"content-type": "application/json"}

        res = requests.post(
            f"http://{self.host}:{self.port}/synthesis",
            data=json.dumps(query_data),
            params=params,
            headers=headers,
        )

        return res.content


    def play_wavfile(self, wav_data: bytes):
        # 音声を再生する
        sample_rate = 24000  # サンプリングレート
        wav_array = np.frombuffer(wav_data, dtype=np.int16)  # バイトデータをnumpy配列に変換
        sd.play(wav_array, sample_rate, blocking=True)  # 音声の再生

    def save_wavfile(self, wav_data: bytes, save_filename: str):
        wav_save_dir = os.environ.get("WAV_SAVE_DIR")
        save_path = os.path.join(wav_save_dir, f"{save_filename}.wav")
        with open(save_path, "wb") as f:
            f.write(wav_data)
        return save_path


    def text_to_voice(self, text: str, savefile_prefix: str):
        # 入力したテキストをVOICEVOXの音声で再生する
        self.logger.debug("text_to_voice: " + text)
        self.logger.debug("post audio query...")
        res = self.post_audio_query(text)
        self.logger.debug("post synthesis...")
        wav = self.post_synthesis(res)
        self.logger.debug("playing wavfile...")
        self.play_wavfile(wav)
        self.logger.debug("saving wavfile...")
        return self.save_wavfile(wav, savefile_prefix)
