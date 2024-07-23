import sys
import streamlit as st
import streamlit.web.cli as stcli

from streamlit import runtime, config


def render() -> None:
    st.set_page_config(
        page_title="Split and generate audio",
        layout="centered",
    )

    module = __import__('split_video_generate_audio', fromlist=["render"])
    module.render()


if __name__ == "__main__":
    st.config.set_option("server.maxUploadSize", 1000)

    if runtime.exists():
        render()
    else:
        sys.argv = ["streamlit", "run"] + sys.argv
        sys.exit(stcli.main())
