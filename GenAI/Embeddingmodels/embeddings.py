import os
from dotenv import load_dotenv  

from langchain.embeddings import OpenAIEmbeddings

load_dotenv()


embeddings = OpenAIEmbeddings(
    model = "text-embedding-3-small",
    dimensions=64
)

text = [
    "What is a database?",
    "What is a vector database?"
    "What is a knowledge graph?"
]

vectors = embeddings.embed_documents(text)
for i, vector in enumerate(vectors):
    print(f"Vector for '{text[i]}': {vector}")