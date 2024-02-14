from datetime import date
import json
import streamlit as st
import cv2
import base64
import os

questions = json.load(open("data/questions.json"))


class Quiz:
    def quiz(self):
        # Define a function to go to the next question
        def next_question():
            # Move to the next question in the questions list
            st.session_state.current_question += 1

            # If we've reached the end of the questions list, get a new question
            if st.session_state.current_question > len(st.session_state.questions) - 1:
                next_question = get_question(st.session_state.current_question)
                st.session_state.questions.append(next_question)
        
        def get_binary_file_downloader_html(bin_file, file_label='File'):
            with open(bin_file, 'rb') as f:
                data = f.read()
            bin_str = base64.b64encode(data).decode()
            href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{os.path.basename(bin_file)}"> Download {file_label}</a>'
            return href
        
        def get_question(index):
            return questions[index]
        
        # Define a function to display the current question and options
        def display_question():
            st.session_state.questions = questions
            # Handle first case
            if len(st.session_state.questions) == 0:
                first_question = get_question(0)
                st.session_state.questions.append(first_question)

            # Disable the submit button if the user has already answered this question
            submit_button_disabled = st.session_state.current_question in st.session_state.answers

            # Get the current question from the questions list
            question = st.session_state.questions[st.session_state.current_question]

            # Display the question prompt
            st.write(f"{st.session_state.current_question + 1}. {question['question']}")

            # Use an empty placeholder to display the radio button options
            options = st.empty()

            # Display the radio button options and wait for the user to select an answer
            user_answer = options.radio("Your answer:", question["options"], key=st.session_state.current_question)

            # Display the submit button and disable it if necessary
            submit_button = st.button("Submit Answer", disabled=submit_button_disabled)

            # If the user has already answered this question, display their previous answer
            if st.session_state.current_question in st.session_state.answers:
                index = st.session_state.answers[st.session_state.current_question]
                options.radio(
                    "Your answer:",
                    question["options"],
                    key=float(st.session_state.current_question),
                    index=index,
                )

            results_placeholder = st.empty()
            # If the user clicks the submit button, check their answer and show the explanation
            if submit_button:
                # Record the user's answer in the session state
                st.session_state.answers[st.session_state.current_question] = question["options"].index(user_answer)

                # Check if the user's answer is correct and update the score
                if user_answer == question["answer"]:
                    results_placeholder.subheader("Correct!")
                    st.session_state.right_answers += 1
                else:
                    results_placeholder.subheader("Incorrect!")
                    st.write(f"Sorry, the correct answer was \n {question['answer']}.")
                    st.session_state.wrong_answers += 1

                # Show an expander with the explanation of the correct answer
                with st.expander("Explanation"):
                    st.write(question["explanation"])
                st.header(f"Score: {st.session_state.right_answers} / {st.session_state.current_question + 1}")

            # Display the current score at the bottom of the page
            st.success(f"Right answers: {st.session_state.right_answers}")
            st.error(f"Wrong answers: {st.session_state.wrong_answers}")

            

        # Initialize session state variables if they don't exist yet
        if "current_question" not in st.session_state:
            st.session_state.answers = {}
            st.session_state.current_question = 0
            st.session_state.questions = []
            st.session_state.right_answers = 0
            st.session_state.wrong_answers = 0
            st.session_state.done_with_quiz = False
            st.session_state.name = ""

        if st.session_state.name == "":
            st.session_state.name = st.text_input("Enter your name")

    
        # Create a 3-column layout for the Prev/Next buttons and the question display
        col2, col3 = st.columns([6, 1])

        # Add a Next button to the right column that goes to the next question
        with col3:
            if col3.button("Next", disabled=st.session_state.done_with_quiz):
                next_question()

        # Display the actual quiz question
        with col2:
            # After getting 68% questions correct and attempting at least 20 questions, display a certificate
            if st.session_state.current_question >= 2 and st.session_state.right_answers/st.session_state.current_question >= 0.68 :
                st.balloons()
                st.success("Congratulations! You have passed the quiz.")
                st.write("Here is your certificate:")
                certi = cv2.imread("data/QU-Certificate-Left aligned.jpg")
                font = cv2.FONT_HERSHEY_DUPLEX 
                fontScale = 2
                original = cv2.putText(certi, st.session_state.name, (80, 510) ,font, fontScale, (0, 0, 0), thickness=2)
                
                original = cv2.putText(original, "Recorded on: "+date.today().strftime('%B %d, %Y'), (650,680) ,font, 0.7, (0, 0, 0), thickness=1)
                cv2.imwrite("Certificate.jpg", original)
                st.image("Certificate.jpg", use_column_width=True)    
                st.markdown(get_binary_file_downloader_html('Certificate.jpg', 'Certificate'), unsafe_allow_html=True)
                st.session_state.done_with_quiz = True              
            else:
                display_question()

        

            
