import streamlit as st
import streamlit_scrollable_textbox as stx


class Video:
    def display_video(self):
        st.subheader("Video", divider="orange")
        st.video("data/Understanding the Amendments and Changes to the Proposed Rules.mp4")

        void, btn_space = st.columns([0.8,0.2])
        with open("./data/transcript.txt", "r") as file:
            data = file.read()
        btn_space.download_button('📩 Transcript', data)    

