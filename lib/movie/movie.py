import os

from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip, AudioFileClip

def craete_movie(telop_str: str, wav_path: str):
    # ffmpegの実行可能ファイルのパスを設定
    os.environ["IMAGEIO_FFMPEG_EXE"] = "/opt/homebrew/bin/ffmpeg"

    # 動画ファイルの読み込み
    video_clip = VideoFileClip(os.environ.get("BACKGROUND_MOVIE_PATH"))

    # 入れる文字を決定する
    txt_clip = TextClip(telop_str,fontsize=70,color='white')

    # 10秒後表示させるテキスト duration:表示する秒数、start：何秒後にスタートさせるか
    text_clip = txt_clip.set_pos('center').set_duration(10).set_start(1)

    # テキストを動画にオーバーレイ
    composite_clip = CompositeVideoClip([video_clip, text_clip])

    # 音声ファイルの読み込み
    audio_clip = AudioFileClip(wav_path)

    # 音声を動画に追加
    final_clip = composite_clip.set_audio(audio_clip)

    # 最終動画の書き出し
    final_clip.write_videofile(os.environ.get("OUTPUT_MOVIE_PATH"))