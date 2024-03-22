# Import libraries
import os
import sys
import re
import streamlit as st
import json
import pandas as pd

class Home:
    ### 
    # This is home page of the application.

    # Change the Application name and Document link in data/config.json by
    # updating parameters "APP_NAME" and "DOCUMENT_LINK"
    
    ###

    def main(self):
        document_link = st.session_state.config_param["DOCUMENT_LINK"]
        st.header(st.session_state.config_param["APP_NAME"], divider= "blue")
        st.markdown("""
        ### Introduction

        - The Department of Consumer and Worker Protection (DCWP) is implementing rules for automated employment decision tools (AEDTs) based on [Local Law 144 of 2021](https://www.nyc.gov/site/dca/about/automated-employment-decision-tools.page).
        - AEDTs cannot be used by employers or employment agencies without undergoing a bias audit and making the audit results public.
        - The bias audit must analyze selection rates for different demographic groups and compare them to detect potential biases.
        - Rules clarify terms, audit requirements, publication standards for audit results, and notice obligations for employees and job candidates.
        - Overall, the rules aim to ensure compliance with the law and promote fairness in employment practices involving AEDTs.
        - It is a process conducted by employers or employment agencies to assess the fairness of an automated employment decision tool (AEDT) in selecting candidates for employment or promotion.
        - It ensures that AEDTs don't unfairly discriminate based on sex, race/ethnicity, or intersectional categories by analyzing selection or scoring patterns and comparing them across demographic groups.
        
        ### Usage Guide

        - Course Materials: Slides and Video of the 8 modules
        - Demo: Bias audit calculations and What-if analysis
        - QuBot: Ask me anything regarding the NY 144 law on Automated Employment Decision Tools (AEDT)
        - Quiz and Certificate: Test your understanding and obtain a certificate of completion
        - Reference PDF: Original publication

        """, unsafe_allow_html=True)
        st.divider()
        st.caption("© 2021 [QuantUniversity](https://www.quantuniversity.com/). All Rights Reserved.")
        st.caption(f"The purpose of this demonstration is solely for educational use and illustration. To access the full legal documentation, please visit [this link]({document_link}). Any reproduction of this demonstration requires prior written consent from QuantUniversity.")
