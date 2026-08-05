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

# Initialize embeddings and LLM globally
embeddings = HuggingFaceEmbeddings(
    model_name='sentence-transformers/all-MiniLM-L6-v2'
)

llm = ChatGroq(
    model='llama-3.3-70b-versatile',
    temperature=0.1,
    groq_api_key=os.environ.get('GROQ_API_KEY'),
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

        # Create or update vectorstore
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
        return self.rag_chain.invoke(question)

rag_service = RAGService()
