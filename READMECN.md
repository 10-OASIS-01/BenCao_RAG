# 🌿本草RAG医药智能助理

🌿本草RAG医药智能助理是一个强大的基于大模型的医药知识问答系统，旨在通过集成上下文感知、互联网访问、知识图谱和检索增强生成来提升用户在知识密集型任务上的体验。即使对大模型了解不足的用户也能轻松利用本系统探索未知知识，享受其带来的乐趣和便利。

<p align="center">
  <img align="middle" src="figure/show.png" style="max-width: 50%; height: auto;" alt="ActiveRAG"/>
</p>

## 功能介绍

本草RAG医药智能助理支持以下功能：

### 💬 基本医药问答
与用户进行互动对话，提供基础医学信息服务，如常见病症的解释和基本治疗建议。

### ⭐ 情境感知医药问答
能够记住用户之前的医学相关对话，并基于上下文提供更相关的医学建议。

### 🌐 互联网搜索增强医药问答
支持互联网访问，能够回答用户关于最新医学研究、药物更新或医疗新闻的查询。

### 📄 文档增强医药问答
支持访问和用户上传的医疗记录、医学文献、临床指南，根据引用的信息为用户查询提供准确的医学答案。

### 🕸️ 医学知识图谱对话系统
在无需依赖大模型的情况下，通过传统方法基于医学知识图谱生成答案，满足用户的特定医学查询需求。

### 🧀 知识图谱增强医药问答
利用医学知识图谱提供更深层次和结构化的医学信息响应，如药物相互作用、病症与治疗方案的关联等。

## 运行步骤

### 1. 安装依赖库
首先，安装项目所需的依赖库：
```sh
pip install -r requirements.txt
```

### 2. 配置 Neo4j
- 下载 Neo4j：[Neo4j 下载中心](https://neo4j.com/download-center/)
- 运行 Neo4j，访问页面：http://localhost:7474（或 7687）
- 设置账户及密码，初始账户和密码均为`neo4j`（`host`类型选择`bolt`）

### 3. 配置OpenAI API-KEY
在utils.py中设置你的api_key，api_base（默认无需设置）和model类型
```
    openai_api_key = ""
    openai_api_base = ""
    model = "gpt-3.5-turbo"
```

### 4. 构建知识图谱
- 导入知识图谱数据（数据来源于：https://github.com/liuhuanyong/QASystemOnMedicalKG ）：
    ```sh
    python KGraph/python/build_medicalgraph.py
    ```
    该过程需要几个小时。

  - 在导入数据之前，需要修改以下内容中的连接协议、用户名和密码：
    - 类AnswerSearcher（KGraph/answer_search.py）
    - 类MedicalGraph（KGraph/build_medicalgraph.py）
    - enhanced_graph（pages/6_🧀_kGraph_enhanced_chatbot.py）
    ```
    self.g = Graph(
        "bolt://localhost:7687",  # 使用 bolt 协议连接
        auth=("neo4j", "your_password")  # 传递用户名和密码
    )
    ```
    ```
    enhanced_graph = Neo4jGraph(url="bolt://localhost:7687", username="neo4j",
                            password="your_password", enhanced_schema=True)
    ```

### 5. 运行本草RAG
- 启动虚拟环境：
    ```sh
    activate xxx
    ```

- 运行 Home.py：
    ```sh
    streamlit run Home.py
    ```

## 结论

🌿本草RAG医药智能助理通过先进的大模型和知识图谱技术，为用户提供全面、准确和个性化的医学信息服务。无论是基础医学问答还是复杂的医学查询，本系统都能够满足用户的需求，助力用户更好地探索和利用医学知识。


## 💁 Contributing

计划随着时间的推移添加更多的聊天机器人示例。欢迎提交PR。在贡献代码时，请创建一个新分支进行修改，不要直接修改master分支。
