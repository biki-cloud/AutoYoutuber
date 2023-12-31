import os
from typing import List

from lib.movie.image import resize
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip, AudioFileClip, CompositeAudioClip, ImageClip, concatenate_audioclips

# 背景に動画を使うかどうか. Falseの場合は画像を使う
is_bg_movie = False
bg_size = (1920, 1080)


def craete_movie(telops: List[str], wav_paths: List[str], logger):
    logger.name = __name__
    # ffmpegの実行可能ファイルのパスを設定
    os.environ["IMAGEIO_FFMPEG_EXE"] = "/opt/homebrew/bin/ffmpeg"

    # 動画ファイルの読み込み. 背景動画の読み込みとループ設定
    # duration: 動画全体の長さ
    if is_bg_movie:
        video_clip = VideoFileClip(os.environ.get("BACKGROUND_MOVIE_PATH"))
        print(video_clip.size) # [1920, 1080]
    else:
        img_path = os.environ.get("BACKGROUND_IMAGE_PATH")
        resize(img_path, bg_size)
        video_clip = ImageClip(img_path)

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
        txt_clip = TextClip(telop, fontsize=50, color='blue', font='/System/Library/Fonts/ヒラギノ明朝 ProN.ttc',
                            bg_color='yellow')
        # duration:表示する秒数、start：何秒後にスタートさせるか
        text_clip = txt_clip.set_pos(('center', 'center')).set_duration(audio_clip.duration).set_start(start_time)
        text_clips.append(text_clip)

        start_time += audio_clip.duration + 1

    # 動画全体の長さを決定
    movie_all_duration = start_time
    logger.debug(f"movie_all_duration: {movie_all_duration}")

    # 背景を動画最後まで設定する
    if is_bg_movie:
        video_clip = video_clip.loop(duration=movie_all_duration)
    else:
        video_clip = video_clip.set_duration(movie_all_duration)

    # 複数のテロップを動画に統合
    composite_clip = CompositeVideoClip([video_clip, *text_clips])

    # BGMを読み込み
    bgm_audio_clip = AudioFileClip(os.environ.get("BGM_MOVIE_PATH"))
    # BGMの長さが動画の長さより短い場合に対応
    if bgm_audio_clip.duration < movie_all_duration:
        # BGMをループさせるためのクリップリストを作成
        bgm_clips = [bgm_audio_clip]
        while sum(clip.duration for clip in bgm_clips) < movie_all_duration:
            bgm_clips.append(bgm_audio_clip)
        # クリップを連結して一つのオーディオクリップにする
        bgm_audio_clip = concatenate_audioclips(bgm_clips)
    # 必要な長さにトリミング
    bgm_audio_clip = bgm_audio_clip.subclip(0, movie_all_duration)
    bgm_audio_clip = bgm_audio_clip.volumex(0.05)
    audio_clips.append(bgm_audio_clip)

    # 複数の音声クリップを統合
    composite_audio = CompositeAudioClip([*audio_clips])

    # 統合された音声をビデオクリップに設定
    video_clip = composite_clip.set_audio(composite_audio)

    # 最終動画の書き出し
    if is_bg_movie:
        video_clip.write_videofile(os.environ.get("OUTPUT_MOVIE_PATH"))
    else:
        video_clip.write_videofile(os.environ.get("OUTPUT_MOVIE_PATH"), fps=24)


if __name__ == "__main__":
    craete_movie("test", "test.wav")
