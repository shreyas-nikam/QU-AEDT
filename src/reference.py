import base64
import streamlit as st


class Reference:
    def __init__(self):
        pdf_file_path = "./data/AEDT.pdf"

        with open(pdf_file_path, "rb") as f:
            pdf_bytes = f.read()

        base64_pdf = base64.b64encode(pdf_bytes).decode('utf-8')

        self.pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width=100% height="1000" type="application/pdf"></iframe>'

    def main(self):
        st.header("💬➡️📈 PDF reference", divider= "blue")
        st.markdown(self.pdf_display, unsafe_allow_html=True)

