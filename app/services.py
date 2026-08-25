import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from dotenv import load_dotenv

load_dotenv()

embeddings = HuggingFaceEmbeddings(
    model_name='sentence-transformers/all-MiniLM-L6-v2'
)

groq_api_key = (os.environ.get('GROQ_API_KEY') or '').strip("'\" ")
groq_model = (os.environ.get('GROQ_MODEL') or 'openai/gpt-oss-120b').strip("'\" ")

llm = ChatGroq(
    model=groq_model,
    temperature=0.1,
    groq_api_key=groq_api_key,
)

prompt = ChatPromptTemplate.from_messages([
    (
        'system',
        'Answer the question using the provided content:\n\nContext:\n{content}',
    ),
    ('human','{question}'),
])

def format_docs(docs):
    return '\n\n'.join(doc.page_content for doc in docs)

class RAGService:
    def __init__(self):
        self.vectorstore = None
        self.retriever = None
        self.rag_chain = None

    def process_pdf(self, file_path: str):
        loader = PyPDFLoader(file_path)
        docs = loader.load()

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size = 1000, chunk_overlap = 200
        )
        splits = text_splitter.split_documents(docs)

        self.vectorstore = Chroma.from_documents(documents=splits, embedding=embeddings)
        self.retriever = self.vectorstore.as_retriever(search_kwargs={'k':3})
        
        self.rag_chain = (
            {'content': self.retriever | format_docs, 'question': RunnablePassthrough()}
            | prompt
            | llm
            | StrOutputParser()
        )

    def chat(self, question: str) -> str:
        if not self.rag_chain:
            return "Please upload a PDF document first."
        try:
            return self.rag_chain.invoke(question)
        except Exception as e:
            err_msg = str(e)
            if "404" in err_msg or "model_not_found" in err_msg or "does not exist" in err_msg:
                return f"Groq API Error: The model '{groq_model}' was not found or your API key does not have access."
            raise e

rag_service = RAGService()
