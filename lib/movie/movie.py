import os
from typing import List

from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip, AudioFileClip, CompositeAudioClip

def craete_movie(telops: List[str], wav_paths: List[str]):
    # ffmpegの実行可能ファイルのパスを設定
    os.environ["IMAGEIO_FFMPEG_EXE"] = "/opt/homebrew/bin/ffmpeg"

    # 動画ファイルの読み込み
    video_clip = VideoFileClip(os.environ.get("BACKGROUND_MOVIE_PATH"))

    telops = ["s" * 100, "s" * 100]
    text_clips = []
    audio_clips = []
    start_time = 1
    for telop, wav_path in zip(telops, wav_paths):
        # ------------------------------
        # 音声ファイルの読み込み
        audio_clip = AudioFileClip(wav_path).set_start(start_time)
        audio_clips.append(audio_clip)

        # 入れる文字を決定する
        txt_clip = TextClip(telop,fontsize=100,color='white')
        # duration:表示する秒数、start：何秒後にスタートさせるか
        text_clip = txt_clip.set_pos(('center', 'center')).set_duration(audio_clip.duration).set_start(start_time)
        text_clips.append(text_clip)

        start_time += audio_clip.duration + 1
    
    
    # 複数のテロップを統合
    composite_clip = CompositeVideoClip([video_clip, *text_clips])

    # 複数の音声クリップを統合
    composite_audio = CompositeAudioClip([*audio_clips])

    # 統合された音声をビデオクリップに設定
    video_clip = composite_clip.set_audio(composite_audio)

    # 最終動画の書き出し
    video_clip.write_videofile(os.environ.get("OUTPUT_MOVIE_PATH"))

if __name__ == "__main__":
    craete_movie("test", "test.wav")