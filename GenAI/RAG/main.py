from dotenv import load_dotenv
from  langchain_mistralai import ChatMistralAI
from langchain_community.document_loaders import TextLoader, PyPDFLoader
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

data = TextLoader("Document_loader/notes.txt")

data2 = PyPDFLoader("Document_loader/GRU.pdf")

docs2 = data2.load()

docs = data.load()

template = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a ai that summarizes text."),
        ("human", "{data2}"),
    ]
)


model = ChatMistralAI(model="mistral-small-latest")


prompt = template.format_prompt(data2=docs2)


result = model.invoke(prompt)

print(result.content)