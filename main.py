from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

llm = ChatOllama(
    model="qwen2.5-coder:3b",
    temperature=0.7,
    

)

# messages= [
#     ("system", "you are a helpful assistant that translates English to French.Translate the user Sentence"),
#     HumanMessage(content=" I love programming."),
# ]
# response = llm.invoke()
# print(response.content)


prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are an expert in {topic}, Give concise, accurate answers."),
        ("human", "{question}")
    ]
)

chain = prompt | llm | StrOutputParser()

for chunk in chain.stream({"topic": "AI", "question": "What is RAG?"}):
    print(chunk, end="", flush=True)