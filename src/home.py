# Import libraries
import os
import sys
import re
import streamlit as st
import json
import pandas as pd
from supabase import create_client, Client
from calculations import Calculations
from whatIf import WhatIf
from chatBot import ChatBot
from quiz import Quiz
from slideDeck import SlideDeck
from video import Video
from reference import Reference
from courseMaterial import CourseMaterial


st.set_option('deprecation.showPyplotGlobalUse', False)

def main():
    page1 = Calculations()
    page2 = WhatIf()
    page3 = ChatBot()
    page4 = Quiz()
    page5 = Reference()
    page6 = CourseMaterial()
    
    url: str = st.secrets["SUPABASE_URL"]
    key: str = st.secrets["SUPABASE_KEY"]
    if 'supabaseDB' not in st.session_state:
        supabase: Client = create_client(url, key)
        st.session_state.supabaseDB = supabase

    if "userInfo" not in st.session_state:
        st.session_state.userInfo = None

    def validate_email(email):
            # Regular expression for basic email validation
            pattern = r'^[a-zA-Z0-9_.+-]+@qusandbox\.com$'
            if re.match(pattern, email):
                return True
            else:
                return False

    # Function to validate full name
    def validate_name(name):
        # Regular expression for name validation (alphabetic characters only)
        pattern = r'^[a-zA-Z ]+$'
        if re.match(pattern, name):
            return True
        else:
            return False
    
    # Set page config
    st.set_page_config(page_title="AEDT Overview",layout="wide", page_icon="▶️")
    st.sidebar.image("https://www.quantuniversity.com/assets/img/logo5.jpg", use_column_width="always")
    page = st.sidebar.radio("Select a Page:", ["Home",  "Course Materials", "Bias Audit Calculations", "What If Analysis", "FAQ - QuBot","Quiz", "Reference PDF"], disabled= True if not st.session_state.userInfo else False)
    
   
    if not st.session_state.userInfo:
        st.header("NY 144 law on Automated Employment Decision Tools (AEDT)", divider= "blue")
        left_co, cent_co,right_co = st.columns([2,3,2])
        with cent_co:
            index = None
            st.markdown("<p style='text-align: center;'>Enter the following information to proceed.</p>", unsafe_allow_html=True)
            name = st.text_input("Name :", placeholder="Enter full name")
            email = st.text_input("Email ID :", placeholder="Enter QuantUniversity email ID")            
            agree = st.checkbox(f"""I read and agree to QuantUniversity's [Privacy Policy](https://www.quantuniversity.com/privacy.html)""")            
            left_co1, cent_co1,right_co1 = cent_co.columns([3,3,3])
            if cent_co1.button('PROCEED'):
                if not name:
                    st.error("Please enter your name.")
                elif not validate_name(name):
                    st.error("Please enter a valid name (alphabetic characters only).")
                elif not email:
                    st.error("Please enter your email.")
                elif not validate_email(email):
                    st.error("Please enter a valid QuantUniversity email address.")
                elif not agree:
                    st.error("Please read and agree the QuantUniversity's [Privacy Policy](https://www.quantuniversity.com/privacy.html).")
                else:
                    data, count = st.session_state.supabaseDB.table('aedt_users').insert({"name":name, "email":email}).execute()
                    st.session_state.userInfo = data[1][0]
                    st.rerun()
    elif page == "Home" :
        st.header("NY 144 law on Automated Employment Decision Tools (AEDT)", divider= "blue")
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
        footer_text = """
        <p style="font-size: 12px; text-align: left">
            Copyright © 2024. All rights reserved by QuantUniversity <br>
            The purpose of this demonstration is solely for educational use and illustration. To access the full legal documentation, please visit <a href="https://www.nyc.gov/site/dca/about/automated-employment-decision-tools.page">this link</a>. Any reproduction of this demonstration requires prior written consent from QuantUniversity.
        </p>
        """
        st.markdown(footer_text, unsafe_allow_html=True)  
        
    if page == "Bias Audit Calculations":        
        page1.main()

    if page == "Course Materials":
        page6.main()

    if page == "What If Analysis":
        page2.main()

    if page == "FAQ - QuBot":
        page3.main()

    if page == "Quiz":
        page4.quiz()

    if page == "Reference PDF":
        page5.main()

if __name__ == "__main__":
    main()
