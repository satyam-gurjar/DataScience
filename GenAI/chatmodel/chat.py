from dotenv import load_dotenv
from langchain_mistralai import ChatMistralAI

load_dotenv()

model = ChatMistralAI(
    model="mistral-small-latest",max_tokens=20, temperature=0.9
)

response = model.invoke("What is a database?")
print(response.content)