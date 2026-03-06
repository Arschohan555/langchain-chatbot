from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

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
        ("system", "You are a helpful AI assistant."),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{question}")
    ]
)

chain = prompt | llm | StrOutputParser()
chat_history =[]
MAX_TURNS = 5

def chat(question):

    current_turns = len(chat_history) // 2
    if current_turns >= MAX_TURNS:
        return(
            "Context window is full"
            "The Ai ma not follow your previous thread properly"
            "Plase type 'clear' for a new chat"
        )
    
    response = chain.invoke({
        "question": question,
        "chat_history":chat_history
    })
    
    chat_history.append(HumanMessage(content=question))
    chat_history.append(AIMessage(content=response))

    remaining = MAX_TURNS - (current_turns + 1)
    if remaining <= 2:
        response += f"\n\nYou {remaining} turn(s) left"

    return response

# print(chat("what is RAG?"))
# print(chat("Give ma a python example of it"))
# print(chat("Now explain the code you just gave"))

def main():
    print("Langchain Chatbot ready! (Type 'quit' for exist, 'clear' reset the history.)")
    while True:
        user_input = input("You:").strip()

        if not user_input:
           continue
        if  user_input.lower()== "quit":
            break
        if user_input.lower() == "clear":
            chat_history.clear()
            print("Chat history cleared.")
            continue

        print("AI:", chat(user_input))  

main()