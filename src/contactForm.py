import streamlit as st
import streamlit.components.v1 as components

class ContactForm:
    def main(self):
        st.header("Contact Form", divider="blue")
        st.write("For any technical issues, comments or feedback, please reach out to us. We would love to hear from you!")
        # contact_form = """
        # <form action="https://formsubmit.co/info@qusandbox.com" method="POST">
        #     <input type="hidden" name="_captcha" value="false">
        #     <input type="hidden" name="course" value="QU-AEDT">
        #     <input type="text" name="name" placeholder="Your name" required>
        #     <input type="email" name="email" placeholder="Your email" required>
        #     <textarea name="message" placeholder="Your message or feedback here"></textarea>
        #     <button type="submit">Send</button>
        # </form>
        # """

        # st.markdown(contact_form, unsafe_allow_html=True)

        components.html("""<iframe src="https://docs.google.com/forms/d/e/1FAIpQLScI4unvhBooDbbGy1mJvFnmkFS29EcG_oGMAlb8ZD4jyyLIRA/viewform?embedded=true" width="640" height="1000" frameborder="0" marginheight="0" marginwidth="0">Loading…</iframe>""", width=640, height=1000)
        def local_css(file_name):
            with open(file_name) as f:
                st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

        local_css("src/contactForm.css")
