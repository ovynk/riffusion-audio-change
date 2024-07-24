import os.path
import sys

import streamlit as st
import streamlit.web.cli as stcli

from streamlit import runtime, config

from utils import get_files_by_regex


def render() -> None:
    st.set_page_config(
        page_title="Split and generate audio",
        layout="centered",
    )

    remove_previous_session_files()

    module = __import__('split_video_generate_audio', fromlist=["render"])
    module.render()


@st.experimental_singleton
def remove_previous_session_files():
    previous_session_files = get_files_by_regex(
        regex=r'(.+\.mp4)|(.+\.zip)|(.+\.wav)',
        directory=os.path.curdir
    )

    if previous_session_files:
        for f in previous_session_files:
            os.remove(f)


if __name__ == "__main__":
    st.config.set_option("server.maxUploadSize", 1000)

    if runtime.exists():
        render()
    else:
        sys.argv = ["streamlit", "run"] + sys.argv
        sys.exit(stcli.main())
