import os
from dotenv import load_dotenv
load_dotenv()
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

loader = PyPDFLoader('Vishnu_Technical_Glossary.pdf')
docs = loader.load()

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size = 1000, chunk_overlap = 200
)
splits = text_splitter.split_documents(docs)

embeddings = HuggingFaceEmbeddings(
    model_name='sentence-transformers/all-MiniLM-L6-v2'
)

vectorstore = Chroma.from_documents(documents=splits, embedding=embeddings)
retriever = vectorstore.as_retriever(search_kwargs={'k':3})


llm = ChatGroq(
    model='llama-3.3-70b-versatile',
    temperature=0.1,
    groq_api_key= os.environ.get('GROQ_API_KEY'),
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


rag_chain = (
    {'content': retriever | format_docs, 'question': RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

query = input('Enter the question you want to ask: ')

response = rag_chain.invoke(query)
print(response)