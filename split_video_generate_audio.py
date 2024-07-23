from model import Model
from utils import get_files_by_regex
from streamlit_utils import *
from video_process import *

print("init model")
model = Model()


def render() -> None:
    with st.sidebar:
        st.write("Additional settings for audio generation")

        device = select_device(st.sidebar)

        negative_prompt = st.text_input("Negative prompt")

        seed = T.cast(int, st.number_input("Seed",
                                           value=1,
                                           help="Use seed to get different audio with same parameters"))

        guidance = st.number_input(
            "Guidance", value=7.0, help="How much the model listens to the text prompt"
        )

        use_20khz = st.checkbox("Use 20kHz", value=False)

    st.subheader("Split and generate audio")

    with st.form("Inputs"):
        prompt = st.text_input("Prompt", value="piano in the sky")

        number_of_clips = T.cast(int, st.number_input("Number of clips", value=2))

        number_change_clip = T.cast(int, st.number_input("Number of the clip you want to change audio", value=2))

        uploaded_file = upload_file(name='uploaded_file.mp4')

        columns_options = [1, 2, 3, 4]
        number_of_clips_to_show = st.selectbox(
            "How many clips to show",
            options=columns_options,
            index=1,
        )

        submit_button = st.form_submit_button("Generate", type="primary")

        if submit_button:
            if not prompt:
                st.info("Enter a prompt")
                return
            if number_of_clips < 1:
                st.info("Number of clips cannot be lower than 1")
                return
            if number_change_clip > number_of_clips or number_change_clip < 1:
                st.info(
                    f"Number of clip you want to change must be lower "
                    f"or equal to {number_of_clips} and higher than 0"
                )
                return
            if uploaded_file is None:
                st.info("Upload video file")
                return
            if seed < 0:
                st.info("Seed cannot be lower than 0")
                return
            if guidance < 0.0 or guidance > 10.0:
                st.info("Guidance should be higher than 0 and lower than 10")
                return

            if uploaded_file is not None:
                splits_names = split_video('uploaded_file.mp4', number_of_clips)
                clip_to_change_name = splits_names[number_change_clip - 1]

                duration_split = VideoFileClip(clip_to_change_name).duration  # seconds

                model.txt2spectrogram(
                    audio_duration=duration_split,
                    prompt=prompt,
                    negative_prompt=negative_prompt,
                    device=device,
                    guidance_scale=guidance,
                    seed=seed
                )

                model.spectrogram2audio(use_20khz=use_20khz)

                set_audio_to_video(audio_path='generated_audio.wav', video_path=clip_to_change_name)

    current_dir = os.path.dirname(os.path.realpath(__file__))
    splits_names = get_files_by_regex(r'(split_).*(\.mp4)', current_dir)

    if splits_names:

        def group_indexes_of_list(li, chunk_size):
            grouped_to_string_indexes = [
                list(range(i, i + len(li[i:i + chunk_size]))) for i in range(0, len(li), chunk_size)
            ]
            return grouped_to_string_indexes

        grouped_indexes_of_splits_names = group_indexes_of_list(splits_names, number_of_clips_to_show)
        splits_to_show = st.selectbox(
            "Select clips to see",
            options=grouped_indexes_of_splits_names,
            index=0,
        )

        download_zip(name_button='Download all clips in zip archive', files=splits_names)

        show_videos(videos_paths=splits_names, indexes_to_show=splits_to_show)
