import os
from typing import List

from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip, AudioFileClip, CompositeAudioClip, ImageClip

def craete_movie(telops: List[str], wav_paths: List[str]):
    # ffmpegの実行可能ファイルのパスを設定
    os.environ["IMAGEIO_FFMPEG_EXE"] = "/opt/homebrew/bin/ffmpeg"

    text_clips = []
    audio_clips = []
    start_time = 1
    for telop, wav_path in zip(telops, wav_paths):
        # ------------------------------
        # 音声ファイルの読み込み
        audio_clip = AudioFileClip(wav_path).set_start(start_time)
        audio_clip = audio_clip.volumex(1.5)
        audio_clips.append(audio_clip)

        # 入れる文字を決定する
        # 日本語対応のフォントを指定しないとてテロップで日本語が表示されない
        txt_clip = TextClip(telop,fontsize=50,color='white',font='/System/Library/Fonts/ヒラギノ明朝 ProN.ttc')
        # duration:表示する秒数、start：何秒後にスタートさせるか
        text_clip = txt_clip.set_pos(('center', 'center')).set_duration(audio_clip.duration).set_start(start_time)
        text_clips.append(text_clip)

        start_time += audio_clip.duration + 1
    
    # 動画ファイルの読み込み. 背景動画の読み込みとループ設定
    # duration: 動画全体の長さ
    video_clip = VideoFileClip(os.environ.get("BACKGROUND_MOVIE_PATH")).loop(duration=start_time)

    # 複数のテロップを統合
    composite_clip = CompositeVideoClip([video_clip, *text_clips])

    # BGMを読み込み
    bgm_audio_clip = AudioFileClip(os.environ.get("BGM_MOVIE_PATH"))
    # オーディオクリップを動画の長さに合わせて調整
    bgm_audio_clip = bgm_audio_clip.subclip(0, video_clip.duration)
    bgm_audio_clip = bgm_audio_clip.volumex(0.05)
    audio_clips.append(bgm_audio_clip)

    # 複数の音声クリップを統合
    composite_audio = CompositeAudioClip([*audio_clips])

    # 統合された音声をビデオクリップに設定
    video_clip = composite_clip.set_audio(composite_audio)

    # 最終動画の書き出し
    video_clip.write_videofile(os.environ.get("OUTPUT_MOVIE_PATH"))

if __name__ == "__main__":
    craete_movie("test", "test.wav")