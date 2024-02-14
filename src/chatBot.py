import os
import time
import streamlit as st
from chat_ui import message_func
from langchain_openai.chat_models import ChatOpenAI
from langchain_core.prompts import PromptTemplate
# from langchain.chains import LLMChain
from langchain_community.vectorstores import FAISS
from langchain.prompts import BasePromptTemplate, PromptTemplate, ChatPromptTemplate, HumanMessagePromptTemplate
from langchain.chains import ConversationChain
from langchain.output_parsers import StructuredOutputParser, ResponseSchema
from langchain_openai import OpenAIEmbeddings



class ChatBot:
    def __init__(self):
        # load_dotenv()
        OPENAI_KEY = st.secrets["OPENAI_KEY"]
        self.OPENAI_MODEL =  st.secrets["OPENAI_MODEL"]
        self.TOTAL_QUES = st.secrets["TOTAL_QUES"]
        # llm = ChatOpenAI(model="gpt-4", temperature=0, api_key=OPENAI_KEY)
        self.embeddings = OpenAIEmbeddings(api_key=OPENAI_KEY)
        self.chatModel = ChatOpenAI(temperature=0, model_name = self.OPENAI_MODEL,openai_api_key = OPENAI_KEY)
        self.chatHistory = """Previous Conversation :\n"""
    
    def get_context(self,query, path = "./data/text_to_vector_db"):
        db = FAISS.load_local(path, self.embeddings)
        docs = db.similarity_search(query)
        return docs

    def get_response(self,question):
        response_schemas = [
                ResponseSchema(name="answer", description="Your answer to the given question",type = 'markdown'),
                ResponseSchema(name="followup_questions", description="A list of 3 insurance related follow-up questions on top the question below.", type = 'list')
            ]
        output_parser = StructuredOutputParser.from_response_schemas(response_schemas)
        format_instructions = output_parser.get_format_instructions()

        context = self.get_context(question)

        prompt = ChatPromptTemplate(
            messages=[
                HumanMessagePromptTemplate.from_template("""
            Answer the given question using the provide context only. Answer the questions in simple financial english. If you 
            You have to return 2 things :
            1. A conversational Reponse to the question below using the context and previous conversation only. 
            2. A list of three insurance related follow-up questions on top the recent question and the answer you will provide. Do not repeat the suggested questions. 
                output format : ['Question1', 'Question2','Question3']

            {format_instructions}

            DONT FORGET TO PUT COMMA(,) between the keys in JSON output

            {history}

            Context:
            {context}

            Question:
            {question} """)
            ],
            input_variables=["history","context","question"],
            partial_variables={"format_instructions": format_instructions}
        )
        _input = prompt.format_prompt(history = self.chatHistory,context = context, question=question)
        output = self.chatModel(_input.to_messages())
        
        validJSON = False
        runs = 0
        while (validJSON == False):
            try:
                json_output = output_parser.parse(output.content)
                validJSON = True
            except Exception as e :
                print(f"Error : {e}")
                runs+=1
                if runs < 4:
                    print(f"\n\n Retry No ::{runs}")
                    error_prompt = ChatPromptTemplate(
                        messages=[
                                HumanMessagePromptTemplate.from_template(""" 
                                Error encountered: {e}

                                Regenerate the previous answer with proper JSON format
                                DO NOT FORGET TO PUT COMMA(,) between the keys in JSON output
                                {format_instructions}

                                {history}

                                Extracted Data:
                                {context}

                                Question:
                                {question} Also include INSURANCE_PLAN_ID if available!""")
                                ],
                        input_variables=["e","history","context","question"],
                        partial_variables={"format_instructions": format_instructions}
                    )
                    _error_input = error_prompt.format_prompt(e=e,history = self.chatHistory,context = context, question=question)
                    print(f"_error_input:: \n{_error_input}")
                    output = self.chatModel(_error_input.to_messages())
                else:
                    return {'answer': f"Something went wrong! Please try again!",
                        'followup_questions': []}
                    

                self.chatHistory += f"""\n
                User : {question}
                Insurance Agent : {str(json_output)}"""
        return json_output

    
            
    def main(self):
        # @st.cache_resource
        
        if "keyOwner" not in st.session_state:
            st.session_state.keyOwner = "QU"


        if "response" not in st.session_state:
            st.session_state.ques_session = True
           
            st.session_state.response = {'answer': 'Hello there! How can I help you today? ',
                            'followup_questions': ["How to calculate impact ratio for a category?",
                                                    "Is an “employment decision” just the final hiring or promotion decision?",
                                                    "What are the parameters required for audit analysis?",
                                                    ]}
        #front-end chatmemory
        INITIAL_MESSAGE = [{"role": "assistant",
                "content": "Hello there! How can I help you today?"}]
        if "messages" not in st.session_state:
            st.session_state["messages"] = INITIAL_MESSAGE

        if "question_per_session" not in st.session_state:
            st.session_state.question_per_session = 0

        def send_prompt(prompt):
            # if "limit_reached" not in st.session_state and st.session_state.question_per_session < self.TOTAL_QUES:
                st.session_state.messages.append({"role": "user", "content": prompt})
                message_func(prompt, is_user =True , is_df=False) #user
                
                with st.spinner('Wait for it...'):
                    time.sleep(1)
                    st.session_state.response = self.get_response(prompt)

                answer = st.session_state.response["answer"]
                st.session_state.messages.append({"role": "assistant", "content": answer})
                st.session_state.ques_session = True
                st.session_state.question_per_session += 1
                if st.session_state.question_per_session == self.TOTAL_QUES:
                    st.session_state.keyOwner = 'None'
                st.rerun()
            

        st.markdown("<h1 style='text-align: center;'>Audit Bias : FAQ Chat Bot</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center;'><i>Disclaimer: This bot is designed to provide insights about audit bais. We strongly recommend to thoroughly read the documents and consult subject matter experts.", unsafe_allow_html=True)
        
        if st.session_state.keyOwner != "None" :
            for message in st.session_state.messages:
                message_func(
                    message["content"],
                    True if message["role"] == "user" else False,
                    True if message["role"] == "data" else False,
                )
            if type(st.session_state.response["followup_questions"]) == str:
                followup_questions = ast.literal_eval(st.session_state.response["followup_questions"])
            else:
                followup_questions = st.session_state.response["followup_questions"]

            col0, col1, col2, col3, col5 = st.columns([0.05,0.30,0.30,0.30,0.05])

            btn1,btn2,btn3 = False,False,False

            if st.session_state.response["followup_questions"] != [] and len(st.session_state.response["followup_questions"]) == 3:
                with col1:
                    ques1 = followup_questions[0]
                    btn1 = st.button(ques1)
                
                with col2:
                    ques2 = followup_questions[1]
                    btn2 = st.button(ques2)

                with col3:
                    ques3 = followup_questions[2]
                    btn3 = st.button(ques3)

            if prompt := st.chat_input():
                    send_prompt(prompt) 

            if btn1:
                send_prompt(ques1)
            if btn2:
                send_prompt(ques2)
            if btn3:
                send_prompt(ques3)
            
            
            print(f"No of questions remaining: {self.TOTAL_QUES - st.session_state.question_per_session}")
            
        else:
            st.warning("You have exhausted your free trial. Enter your OpenAI key below to conitnue")
            # input_content, btn_content = st.columns([0.8,0.2])
            OPENAI_KEY = st.text_input('OpenAI key:',type="password")

            if st.button("Submit Key", type="secondary"):
                self.chatModel = ChatOpenAI(temperature=0, model_name = self.OPENAI_MODEL,openai_api_key = OPENAI_KEY)
                st.session_state.keyOwner = "USER"
                st.rerun()

        


            