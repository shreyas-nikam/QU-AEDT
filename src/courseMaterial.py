import streamlit as st
from video import Video
from slideDeck import SlideDeck

class CourseMaterial:
    def main(self):
        if "showVideo" not in st.session_state:
            st.session_state.showVideo = True
        
        st.header("Course Material", divider="blue")

        btn_video, btn_slide, void ,btn_download = st.columns([0.08,0.08,0.75,0.15])
        if btn_video.button("Video", disabled = st.session_state.showVideo):
            st.session_state.showVideo = True
            st.rerun()
        if btn_slide.button("Slide", disabled = not st.session_state.showVideo):
            st.session_state.showVideo = False
            st.rerun()

        if st.session_state.showVideo:
            st.subheader("Video", divider="orange")
            st.video("data/Understanding the Amendments and Changes to the Proposed Rules.mp4")
        else :
            slides = SlideDeck()
            slides.display_deck()       

        with open("./data/transcript.txt", "r") as file:
            data = file.read()
        btn_download.download_button('📩 Transcript', data)