import streamlit as st
import streamlit.components.v1 as components

class SlideDeck:
    def __init__(self):
        self.course_links = [
            "https://docs.google.com/presentation/d/e/2PACX-1vRMHuTJz9l3H2L7_j-xR8S2WVE01NEyuyYQrdH9lAi5MkO_Q7WioU97t5zBCCAeOg/embed?start=false&loop=false&delayms=3000",
            "https://docs.google.com/presentation/d/e/2PACX-1vSH7JAHpAHX9iYeEEUZ3prMumw1e--5t-x5Ce7Pq7XXcqjHvAsRj0HVSrWwty1LOQ/embed?start=false&loop=false&delayms=3000",
            "https://docs.google.com/presentation/d/e/2PACX-1vTJS4uy5QIvd_wGVpg860zmVFJkszUDEJ0TmuqPRqpMJWehDugCHJfy9W5q71TAFQ/embed?start=false&loop=false&delayms=3000",
            "https://docs.google.com/presentation/d/e/2PACX-1vQvIGe4BiYhpHMIPJlza-g_xMeMRAS6EhjJhoAINexofhlbjWT8sJkqPyiUCVwZGA/embed?start=false&loop=false&delayms=3000",
            "https://docs.google.com/presentation/d/e/2PACX-1vRtOdmBe4WecHGGm8EaVuuirzB4jyjZ1Aw-vOvlx09b7XV-q-nOBbpqfIc3V0v3hQ/embed?start=false&loop=false&delayms=3000",
            "https://docs.google.com/presentation/d/e/2PACX-1vSKRqROyuJrT1Ok2yX-Nw0ipy9KkjeROURIUNeB_LpajPibAZiuQ4O-cXm3UtWt2w/embed?start=false&loop=false&delayms=300",
            "https://docs.google.com/presentation/d/e/2PACX-1vTx8HL2lTD86KtrsYlraxUAnPIs4oWPbguFwasto4SjoleQcbf--q1AsmyMGQh-iQ/embed?start=false&loop=false&delayms=3000",
            "https://docs.google.com/presentation/d/e/2PACX-1vRYFcd9XwNl8kIu6SSOU-WpoQTwlQSi8CRM_HUSjtoPfStF9yhrNMqqth5GddTPew/embed?start=false&loop=false&delayms=3000"
        ]
    def display_deck(self):
        if "course_index" not in st.session_state:
            st.session_state.course_index = 0
        # st.session_state.course_index = 0

        st.subheader(f"Slide Deck - Module {st.session_state.course_index+1}", divider="orange")
        
        components.iframe(self.course_links[st.session_state.course_index],  height=560)
        
        col1, col2, col3 = st.columns([0.1, 0.6,0.1])
        with col1:
            if st.session_state.course_index>0:
                
                if st.button("Previous Module"):
                    st.session_state.course_index-=1
                    st.rerun()
        
    
        with col3:
            if st.session_state.course_index<len(self.course_links):
                
                if st.button("Next Module"):
                    st.session_state.course_index+=1
                    st.rerun()