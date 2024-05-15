import utils
import streamlit as st
from streaming import StreamHandler

from langchain_openai import ChatOpenAI
from langchain.chains import ConversationChain
from KGraph.question_classifier import *
from KGraph.question_parser import *
from KGraph.answer_search import *

st.set_page_config(page_title="医学知识图谱对话系统", page_icon="🕸️")
st.header('🕸️医学知识图谱对话系统')
st.write('在无需依赖大模型的情况下，通过传统方法基于医学知识图谱生成答案，满足用户的特定医学查询需求。')

class ChatBotGraph:
    def __init__(self):
        self.classifier = QuestionClassifier()
        self.parser = QuestionPaser()
        self.searcher = AnswerSearcher()

    def chat_main(self, sent):
        answer = '您好，我是本草RAG医药智能助理，希望可以帮到您。祝您身体棒棒！'
        res_classify = self.classifier.classify(sent)
        if not res_classify:
            return answer
        res_sql = self.parser.parser_main(res_classify)
        final_answers = self.searcher.search_main(res_sql)
        if not final_answers:
            return answer
        else:
            return '\n'.join(final_answers)

class Basic:
    def __init__(self):
        self.handler = ChatBotGraph()
    @utils.enable_chat_history
    def main(self):

        prompt = st.chat_input("您好，我是本草RAG医药智能助理，希望可以帮到您。祝您身体棒棒！")
        # React to user input
        if prompt:
            # Display user message in chat message container
            st.chat_message("user").markdown(prompt)
            # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": prompt})

            response = self.handler.chat_main(prompt)
            # Display assistant response in chat message container
            with st.chat_message("assistant"):
                st.markdown(response)
            # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": response})


if __name__ == "__main__":
    obj = Basic()
    obj.main()




