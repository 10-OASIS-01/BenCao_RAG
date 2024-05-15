import utils
import streamlit as st
from streaming import StreamHandler

from langchain_openai import ChatOpenAI
from langchain.chains import ConversationChain

st.set_page_config(page_title="基本医药问答", page_icon="💬")
st.header('💬基本医药问答')
st.write('与用户进行互动对话，提供基础医学信息服务，如常见病症的解释和基本治疗建议')

class Basic:

    def __init__(self):
        self.openai_model = utils.configure_openai()
    
    def setup_chain(self):
        llm = ChatOpenAI(model_name=self.openai_model, temperature=0.2, streaming=True)
        chain = ConversationChain(llm=llm, verbose=True)
        return chain
    
    @utils.enable_chat_history
    def main(self):
        chain = self.setup_chain()
        user_query = st.chat_input(placeholder="您好，我是本草RAG医药智能助理，希望可以帮到您。祝您身体棒棒！")
        if user_query:
            utils.display_msg(user_query, 'user')
            with st.chat_message("assistant"):
                st_cb = StreamHandler(st.empty())
                result = chain.invoke(
                    {"input":user_query},
                    {"callbacks": [st_cb]}
                )
                response = result["response"]
                st.session_state.messages.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    obj = Basic()
    obj.main()