# Bài 27: RAG, Agents & LLM Applications

## 🎯 Mục tiêu
- RAG (Retrieval-Augmented Generation) — kỹ thuật quan trọng nhất
- LLM Agents: tool use, function calling
- Xây dựng ứng dụng LLM production-ready

---

## 1. RAG — Retrieval-Augmented Generation

### 1.1 Tại sao cần RAG?
```
LLM problems:
- Hallucination: bịa thông tin
- Knowledge cutoff: không biết dữ liệu mới
- No private data: không biết tài liệu nội bộ

RAG solution:
1. Lưu tài liệu vào vector database
2. Khi user hỏi → tìm documents liên quan
3. Đưa documents + câu hỏi cho LLM → trả lời chính xác
```

### 1.2 RAG Pipeline
```python
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.chains import RetrievalQA

# Step 1: Load documents
loader = PyPDFLoader("company_docs.pdf")
documents = loader.load()

# Step 2: Split into chunks
splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
chunks = splitter.split_documents(documents)

# Step 3: Create embeddings & store in vector DB
embeddings = OpenAIEmbeddings()
vectorstore = Chroma.from_documents(chunks, embeddings, persist_directory="./chroma_db")

# Step 4: Query
retriever = vectorstore.as_retriever(search_kwargs={"k": 5})
llm = ChatOpenAI(model="gpt-4", temperature=0)

qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=retriever,
    return_source_documents=True,
)

result = qa_chain.invoke({"query": "Chính sách nghỉ phép như thế nào?"})
print(result["result"])
```

### 1.3 RAG nâng cao
```python
# 1. Hybrid search: keyword (BM25) + semantic (vector)
from langchain.retrievers import EnsembleRetriever
from langchain_community.retrievers import BM25Retriever

bm25 = BM25Retriever.from_documents(chunks, k=5)
vector_retriever = vectorstore.as_retriever(search_kwargs={"k": 5})
ensemble = EnsembleRetriever(retrievers=[bm25, vector_retriever], weights=[0.4, 0.6])

# 2. Reranking: rank lại kết quả search
# Dùng Cohere Rerank hoặc cross-encoder

# 3. Chunking strategies:
# - Fixed size (đơn giản)
# - Recursive character (tốt hơn)
# - Semantic chunking (tốt nhất, dùng embeddings)
```

---

## 2. LLM Agents

### 2.1 Concept
```
Agent = LLM + Tools + Memory + Planning

LLM quyết định:
1. Cần tool gì? (search, calculator, code execution...)
2. Gọi tool với parameters gì?
3. Dùng kết quả tool để trả lời

Framework: ReAct (Reasoning + Acting)
Thought → Action → Observation → Thought → ... → Answer
```

### 2.2 Function Calling
```python
from openai import OpenAI

client = OpenAI()

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get current weather for a location",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {"type": "string", "description": "City name"},
                },
                "required": ["location"],
            },
        },
    }
]

response = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "What's the weather in Hanoi?"}],
    tools=tools,
)

# LLM sẽ trả về function call: get_weather(location="Hanoi")
# Bạn thực thi function → trả kết quả cho LLM → LLM trả lời user
```

### 2.3 Agent với LangChain
```python
from langchain.agents import create_react_agent, AgentExecutor
from langchain.tools import Tool
from langchain_community.utilities import SerpAPIWrapper

# Define tools
search = SerpAPIWrapper()
tools = [
    Tool(name="Search", func=search.run, description="Search the internet"),
    Tool(name="Calculator", func=lambda x: eval(x), description="Math calculations"),
]

# Create agent
agent = create_react_agent(llm, tools, prompt_template)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

result = agent_executor.invoke({"input": "What is the GDP of Vietnam in 2024, and what's 15% of that?"})
```

---

## 3. Prompt Engineering

```python
# 1. Zero-shot
prompt = "Classify the sentiment: 'This movie is great!' → "

# 2. Few-shot
prompt = """
Classify sentiment:
'I love it' → Positive
'Terrible product' → Negative
'Not bad' → Positive
'This food is amazing!' → """

# 3. Chain-of-Thought (CoT)
prompt = """
Q: A store has 5 apples. It sells 2 and receives 8 more. How many apples?
Let's think step by step:
1. Start: 5 apples
2. Sell 2: 5 - 2 = 3
3. Receive 8: 3 + 8 = 11
Answer: 11

Q: A library has 120 books. It lends 45 and receives 30 donations. How many?
Let's think step by step:
"""

# 4. System prompt
messages = [
    {"role": "system", "content": "You are a Vietnamese legal expert. Always cite relevant laws."},
    {"role": "user", "content": "Luật lao động quy định giờ làm việc như thế nào?"},
]
```

---

## 4. Evaluation

```python
# Automated metrics
from rouge_score import rouge_scorer
scorer = rouge_scorer.RougeScorer(['rouge1', 'rougeL'], use_stemmer=True)
scores = scorer.score("reference text", "generated text")

# LLM-as-Judge
judge_prompt = """
Rate the following answer on a scale of 1-5:
Question: {question}
Answer: {answer}
Reference: {reference}

Score (1-5) and explain:
"""
```

---

## 📝 Bài tập

1. **RAG Chatbot**: Xây dựng chatbot hỏi đáp cho PDF tài liệu pháp luật VN
2. **Agent**: Tạo agent có thể search web + đọc file + tính toán
3. **Prompt Engineering**: Tối ưu prompt cho task classification tiếng Việt
4. **Full Application**: Deploy RAG app với Streamlit/Gradio

---

## 📚 Tài liệu
- [LangChain Documentation](https://python.langchain.com/)
- [LlamaIndex Documentation](https://docs.llamaindex.ai/)
- *Building LLM Applications* — Chip Huyen
- *Prompt Engineering Guide* (promptingguide.ai)
