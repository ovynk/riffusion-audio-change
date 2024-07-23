import zipfile
import typing as T

import torch
import streamlit as st

from video_process import write_bytesio_to_file


def select_device(container: T.Any = st.sidebar) -> str:
    """
    Dropdown to select a torch device, with an intelligent default.
    """
    default_device = "cpu"
    if torch.cuda.is_available():
        default_device = "cuda"
    elif torch.backends.mps.is_available():
        default_device = "mps"

    device_options = ["cuda", "cpu", "mps"]
    device = st.sidebar.selectbox(
        "Device",
        options=device_options,
        index=device_options.index(default_device),
        help="Which compute device to use. CUDA is recommended.",
    )
    assert device is not None

    return device


def upload_file(name):
    uploaded_file = st.file_uploader("Choose a file")

    if uploaded_file is not None:
        # To read file as bytes
        bytes_data = uploaded_file.getvalue()

        write_bytesio_to_file(name, bytes_data)

        return bytes_data


def download_zip(name_button, files):
    def zipdir(files, ziph):
        # ziph is zipfile handle
        for file in files:
            ziph.write(file)

    with zipfile.ZipFile('clips.zip', 'w', zipfile.ZIP_DEFLATED) as zipf:
        zipdir(files, zipf)

    with open("clips.zip", "rb") as file:
        btn = st.download_button(
            label=name_button,
            data=file,
            file_name="clips.zip",
        )


def show_videos(videos_paths: list, indexes_to_show: list):
    """
    Shows videos in columns and rows. Maximum is 4 videos.
    It is made to reduce length, size of the page.

    :parameter videos_paths list of video names with its extension.
    :parameter indexes_to_show list of index to show from video_paths.
    It must be length of 1, 2, 3 or 4. For example: video_paths is 10 length.
    I want to see 7, 8, 9 videos from list. indexes_to_show will be [7, 8, 9]
    """

    if len(indexes_to_show) not in [1, 2, 3, 4]:
        print("indexes_to_show must be length of 1, 2, 3 or 4")
        return

    if len(indexes_to_show) == 4:
        columns = st.columns(2)

        for i, column in enumerate(columns):
            with column:
                clip_upper = i * 2
                clip_bottom = i * 2 + 1

                st.subheader(f'clip {indexes_to_show[clip_upper]}')
                st.video(videos_paths[indexes_to_show[clip_upper]])

                st.subheader(f'clip {indexes_to_show[clip_bottom]}')
                st.video(videos_paths[indexes_to_show[clip_bottom]])
    elif len(indexes_to_show) == 3:
        columns = st.columns(1)

        with columns[0]:
            st.subheader(f'clip {indexes_to_show[0]}')
            st.video(videos_paths[indexes_to_show[0]])

            st.subheader(f'clip {indexes_to_show[1]}')
            st.video(videos_paths[indexes_to_show[1]])

            st.subheader(f'clip {indexes_to_show[2]}')
            st.video(videos_paths[indexes_to_show[2]])
    else:
        columns = st.columns(len(indexes_to_show))

        for i, column in enumerate(columns):
            with column:
                st.subheader(f'clip {indexes_to_show[i]}')
                st.video(videos_paths[indexes_to_show[i]])
