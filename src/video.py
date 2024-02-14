import streamlit as st
import streamlit_scrollable_textbox as stx


class Video:
    def display_video(self):
        st.header("Video", divider="blue")
        st.video("data/Understanding the Amendments and Changes to the Proposed Rules.mp4")
        st.subheader("Transcript:")
        transcript = open("data/transcript.txt").read()
        stx.scrollableTextbox(transcript,height = 300)

