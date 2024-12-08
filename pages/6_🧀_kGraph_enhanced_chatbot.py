import utils
import streamlit as st
from streaming import StreamHandler
from langchain_community.graphs import Neo4jGraph
from langchain_openai import ChatOpenAI
from langchain.chains import GraphCypherQAChain
from langchain_core.prompts import ChatPromptTemplate
from langchain.memory import ConversationBufferMemory

st.set_page_config(page_title="知识图谱增强医药问答", page_icon="🧀")
st.header('🧀知识图谱增强医药问答')
st.write('利用医学知识图谱提供更深层次和结构化的医学信息响应，如药物相互作用、病症与治疗方案的关联等。')


class Basic:

    def __init__(self):
        self.openai_model = utils.configure_openai()

    # @st.cache_resource
    def setup_chain(self):
        st.empty()
        memory = ConversationBufferMemory()
        llm = ChatOpenAI(model_name=self.openai_model, temperature=0.2, streaming=True)
        chain = GraphCypherQAChain.from_llm(llm=llm, graph=enhanced_graph,
                                            verbose=False, validate_cypher=True,
                                            return_direct=True, memory=memory)
        return chain

    def qa_chain(self):
        prompt = ChatPromptTemplate.from_template("你是一个AI医生，只通过分析{pre_result}的内容来为对方询问的{query}问题提供专业建议。"
                                                  "直接建议"
                                                  "使用{pre_result}中的词或者句子")
        llm = ChatOpenAI(model_name=self.openai_model, temperature=0.2, streaming=True, max_tokens=1000)
        chain = prompt | llm
        return chain

    @utils.enable_chat_history
    def main(self):
        # from neo4j.exceptions import CypherSyntaxError
        chain = self.setup_chain()
        qa_chain = self.qa_chain()
        user_query = st.chat_input(placeholder="您好，我是本草RAG医药智能助理，希望可以帮到您。祝您身体棒棒！")
        if user_query:
            utils.display_msg(user_query, 'user')
            with st.chat_message("assistant"):
                st_cb = StreamHandler(st.empty())
                try:
                    result = chain.invoke(
                        {"query": user_query},
                    )
                    print(f"{result}\n")
                except BaseException as e:
                    result = {"query": user_query, "result": []}
                result_qa = qa_chain.invoke({"pre_result": result['result'], "query": result['query']},
                                            {"callbacks": [st_cb]})
                response = result_qa.content
                st.session_state.messages.append({"role": "assistant", "content": response})


enhanced_graph = Neo4jGraph(url="bolt://localhost:7687", username="neo4j",
                            password="your_password", enhanced_schema=True)

if __name__ == "__main__":
    obj = Basic()
    obj.main()

