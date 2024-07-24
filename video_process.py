import os
import numpy as np
import moviepy.utils

from moviepy.editor import VideoFileClip, AudioFileClip


def write_bytesio_to_file(filename, bytesio):
    """
    Write the contents of the given BytesIO to a file.
    Creates the file or overwrites the file if it does
    not exist yet.
    """
    with open(filename, "wb") as outfile:
        outfile.write(bytesio)


def split_video(video_path, splits):
    """
    :param video_path: str path to video
    :param splits: number of videos after splitting
    :return: list of splits names
    """
    if splits < 2:
        print("Number of splits cannot be lower than 2.")
        return

    splits_names = []

    video = VideoFileClip(video_path)
    duration = video.duration
    duration_of_split = duration / splits

    clip = None
    for i, time in enumerate(np.arange(0.0, duration, duration_of_split)):
        split_name = f"split_{i}.mp4"
        splits_names.append(split_name)

        clip = video.subclip(time, time+duration_of_split)
        clip.write_videofile(split_name)

    clip.close()
    video.close()
    moviepy.utils.close_all_clips()

    return splits_names


def set_audio_to_video(audio_path, video_path) -> None:
    """
    Takes audio and video paths.
    Creates new video with set audio. Then removes original
    and renames new video to original name.
    """
    video = VideoFileClip(video_path)
    audio = AudioFileClip(audio_path)

    audio = audio.subclip(0.0, video.duration)

    new_video = video.set_audio(audio)
    new_video.write_videofile(filename='clip_new_audio.mp4')

    new_video.close()
    video.close()
    audio.close()
    moviepy.utils.close_all_clips()

    os.remove(video_path)

    os.rename('clip_new_audio.mp4', video_path)
