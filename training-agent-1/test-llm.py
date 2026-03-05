# from langchain_ollama import ChatOllama

# llm = ChatOllama(model="llama3:latest", temperature=0.3)

# print(llm.invoke("Hello"))

from langchain_ollama import ChatOllama

llm = ChatOllama(model="llama3")

prompt = "Explain Python functions in 2 lines"

response = llm.invoke(prompt)

print("\nResponse:\n")
print(response.content)