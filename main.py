import json
import streamlit as st
import pandas as pd
from src.home import Home
from src.chatBot import ChatBot
from src.courseMaterial import CourseMaterial
from src.reference import Reference
from src.quiz import Quiz
from src.whatIf import WhatIf
from src.calculations import BiasAuditCalculations
from src.contactForm import ContactForm

if "user_info" not in st.session_state:
    st.session_state.user_info = {}
    st.switch_page("pages/login.py")



if "config_param" not in st.session_state:
    with open("./data/config.json", 'r') as file:
        json_data = file.read()
    st.session_state.config_param = json.loads(json_data)

if "page_chatbot" not in st.session_state:
    st.session_state.page_chatbot = ChatBot()
    st.session_state.page_home = Home()
    st.session_state.page_quiz = Quiz()
    st.session_state.page_reference = Reference()
    st.session_state.page_courseMaterial = CourseMaterial()
    st.session_state.page_calculations = BiasAuditCalculations()
    st.session_state.page_whatIf = WhatIf()
    st.session_state.contact_form = ContactForm()


st.set_page_config(
    page_title=st.session_state.config_param["APP_NAME"], layout="wide", page_icon="🏬")
st.sidebar.image(
    "https://www.quantuniversity.com/assets/img/logo5.jpg", use_column_width="always")



_, logout_button_space = st.columns([0.9, 0.1])
if logout_button_space.button("Logout", use_container_width=True, type="primary"):
    for key in st.session_state.keys():
        del st.session_state[key]
    st.switch_page("pages/login.py")


# Set sidebar routes
page = st.sidebar.radio(label="Select a Page:",
                        options=["Home",
                        #  "Course Material",
                         "Bias Audit Calculations",
                         "What If Analysis",
                         "QuBot",
                         "Quiz",
                        #  "Reference PDF", 
                         "Contact Form"],
                        disabled=True if not st.session_state.user_info else False)

# check if the content is updated

if page == "Home":
    st.session_state.page_home.main()
# elif page == "Course Material":
#     st.session_state.page_courseMaterial.main()
elif page == "QuBot":
    st.session_state.page_chatbot.main()
elif page == "Quiz":
    st.session_state.page_quiz.main()
elif page == "Bias Audit Calculations":
    if "page_calculations" in st.session_state:
        st.session_state.page_calculations.main()
    else:
        st.session_state.page_calculations = BiasAuditCalculations()
        st.session_state.page_calculations.main()
elif page == "What If Analysis":
    if "page_whatIf" in st.session_state:
        st.session_state.page_whatIf.main()
    else:
        st.session_state.page_whatIf = WhatIf()
        st.session_state.page_whatIf.main()
# elif page == "Reference PDF":
#     st.session_state.page_reference.main()
elif page == "Contact Form":
    st.session_state.contact_form.main()
        
