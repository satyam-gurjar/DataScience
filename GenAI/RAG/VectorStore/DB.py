from langchain_mistralai import MistralAIEmbeddings
from langchain_community.vectorstores import Chroma
from dotenv import load_dotenv

load_dotenv()

from  langchain_core.documents import Document


docs = [
    Document(page_content="python is a programming language.use it to create artificial intelligence applications", metadata={"source": "file1.txt"}), 
    Document(page_content="In python panda is used for data analysis", metadata={"source": "file2.txt"}),
    Document(page_content="python is use for machine learning", metadata={"source": "file3.txt"})
    
]

# Initialize the MistralAIEmbeddings
embedding_model = MistralAIEmbeddings()

# Create a Chroma vector store and add the documents
vectorstore = Chroma.from_documents(
    documents= docs, 
    embedding = embedding_model,
    persist_directory="./chroma_db"
)


result = vectorstore.similarity_search("what is use of python", k=2)

for r in result:
    print(r.page_content)
