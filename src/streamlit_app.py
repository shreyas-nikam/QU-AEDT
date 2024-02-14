# Import libraries
import os
import sys
import streamlit as st
import json
import pandas as pd
from biasAuditCalculations import BiasAuditCalculations
from whatIf import WhatIf
# from chatBot import ChatBot
# from quiz import Quiz
from slideDeck import SlideDeck
from video import Video
from reference import Reference

st.set_option('deprecation.showPyplotGlobalUse', False)

def main():
    # Set page config
    st.set_page_config(page_title="AEDT Overview",layout="wide", page_icon="▶️")
    st.sidebar.image("https://www.quantuniversity.com/assets/img/logo5.jpg", use_column_width="always")
    page = st.sidebar.radio("Select a Page:", ["Home",  "Video", "Slide Deck", "Bias Audit Calculations", "What If Analysis", "Chat Bot","Quiz", "Reference PDF"])
    
    if page == "Home":
        st.header("💬➡️📈NY 144 law on Automated Employment Decision Tools (AEDT)", divider= "blue")
        st.caption("Please refer to the [user guide]() on information to navigate the application.")
        
        st.markdown("""
        ### Introduction

        - The Department of Consumer and Worker Protection (DCWP) is implementing rules for automated employment decision tools (AEDTs) based on Local Law 144 of 2021.
        - AEDTs cannot be used by employers or employment agencies without undergoing a bias audit and making the audit results public.
        - The bias audit must analyze selection rates for different demographic groups and compare them to detect potential biases.
        - Rules clarify terms, audit requirements, publication standards for audit results, and notice obligations for employees and job candidates.
        - Overall, the rules aim to ensure compliance with the law and promote fairness in employment practices involving AEDTs.
        - It is a process conducted by employers or employment agencies to assess the fairness of an automated employment decision tool (AEDT) in selecting candidates for employment or promotion.
        - It ensures that AEDTs don't unfairly discriminate based on sex, race/ethnicity, or intersectional categories by analyzing selection or scoring patterns and comparing them across demographic groups.

        """)

        st.divider()
        footer_text = """
        <p style="font-size: 10px; text-align: center">
            Copyright © 2024. All rights reserved by QuantUniversity <br>
            The purpose of this demonstration is solely for educational use and illustration. To access the full legal documentation, please visit <a href="https://www.nyc.gov/site/dca/about/automated-employment-decision-tools.page">this link</a>. Any reproduction of this demonstration requires prior written consent from QuantUniversity.
        </p>
        """
        st.markdown(footer_text, unsafe_allow_html=True)  
        
    page1 = BiasAuditCalculations()
    page2 = WhatIf()
    # page3 = ChatBot()
    # page4 = Quiz()
    page5 = Reference()

    if page == "Bias Audit Calculations":        
        page1.main()

    if page == "What If Analysis":
        page2.main()

    # if page == "Chat Bot":
    #     page3.main()

    # if page == "Quiz":
    #     page4.quiz()

    if page == "Reference PDF":
        page5.main()

    if page == "Slide Deck":
        slides = SlideDeck()
        slides.display_deck()
    
    if page == "Video":
        video  = Video()
        video.display_video()


          
if __name__ == "__main__":
    main()
