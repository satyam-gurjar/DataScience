#load the pdf  
#split the pdf into chunks
#create the embeddings for the chunks
#store the embeddings in a vector database

from langchain_community.document_loaders import TextLoader, PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_mistralai import ChatMistralAI,MistralAIEmbeddings
from langchain_community.vectorstores import Chroma
from dotenv import load_dotenv
load_dotenv()

loader = PyPDFLoader("Document_loader/deeplearning.pdf")
docs = loader.load()

splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)

chunks = splitter.split_documents(docs)

embedding_model = MistralAIEmbeddings()


vectorstore = Chroma.from_documents(
    documents= chunks,
    embedding = embedding_model,
    persist_directory="./chroma_db"
)