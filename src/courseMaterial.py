import streamlit as st
from video import Video
from slideDeck import SlideDeck

class CourseMaterial:
    def __init__(self):
        self.slides = SlideDeck()
    def main(self):
        
        st.header("Course Material", divider="blue")

        tab_video, tab_slide = st.tabs(["Video", "Slides"])
        with tab_video: 
            st.video("data/Understanding the Amendments and Changes to the Proposed Rules.mp4")
            void, btn_space = st.columns([0.8,0.2])
            with open("./data/transcript.txt", "r") as file:
                data = file.read()
            btn_space.download_button('📩 Download Transcript', data)  
                
        with tab_slide: 
            self.slides.display_deck()       
    