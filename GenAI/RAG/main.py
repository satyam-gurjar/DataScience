from dotenv import load_dotenv
from  langchain_mistralai import ChatMistralAI
from langchain_community.document_loaders import TextLoader, PyPDFLoader
from langchain_core.prompts import ChatPromptTemplate
from langchain_text_splitters import RecursiveCharacterTextSplitter


load_dotenv()


data = PyPDFLoader("Document_loader/deeplearning.pdf")
docs = data.load()

splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)

chunks = splitter.split_documents(docs)

template = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a ai that summarizes text."),
        ("human", "{data}"),
    ]
)


model = ChatMistralAI(model="mistral-small-latest")


prompt = template.format_prompt(data=chunks )


result = model.invoke(prompt)

print(result.content)