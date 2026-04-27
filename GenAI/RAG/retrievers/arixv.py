from langchain_community.retrievers import ArxivRetriever

#create the retriever
retriever = ArxivRetriever(
    load_max_docs= 2,
    load_all_available_meta=True
)

#query the retriever

docs = retriever.invoke("large language models")

#print the retrieved documents
for i, doc in enumerate(docs):
    print(f"Document {i+1}:")
    print(f"Title: {doc.metadata.get('Title')}")
    print(f"Authors: {', '.join(doc.metadata.get('authors', []))}")
    print(f"Abstract: {doc.metadata.get('abstract')}")
    print(f"URL: {doc.metadata.get('url')}")
    print("summary: ", doc.page_content[:500], "...")
    print("\n")
