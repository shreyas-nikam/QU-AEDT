import streamlit as st
from src.s3FileManager import S3FileManager

class MyReports:
    def __init__(self):
        self.s3_file_manager = S3FileManager()

    def display_report(self, report):
        name_col, date_col, size_col, delete_button_col, download_button_col = st.columns([4, 2, 2, 1, 1])
        name_col.write(report[0])
        date_col.write(report[1])
        size_col.write(report[2])
        if delete_button_col.button("Delete"):
            self.s3_file_manager.delete_report(report[0], st.session_state.user_info['email'])
            st.rerun()
        if download_button_col.button("Download"):
            
    

    def main(self):
        # fetch reports
        # display reports - delete , rename, download report, view report in new tab.
        st.header("My Reports", divider='blue')
        reports = self.s3_file_manager.get_reports_list()
        if len(reports) == 0:
            st.write("No reports available.")
        else:
            for report in reports:
                self.display_report(report)