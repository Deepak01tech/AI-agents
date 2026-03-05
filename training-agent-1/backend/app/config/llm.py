# from langchain_openai import ChatOpenAI
# from dotenv import load_dotenv
# import os

# load_dotenv()

# api_key = os.getenv("OPENAI_API_KEY")

# if not api_key:
#     raise ValueError("OPENAI_API_KEY not found in environment variables")

# llm = ChatOpenAI(
#     model="gpt-4o-mini",
#     api_key=api_key,
#     temperature=0.3
# )

from langchain_ollama import ChatOllama

llm = ChatOllama(
    model="gemma3:4b",
    temperature=0.3
)

# from langchain_anthropic import ChatAnthropic
# from dotenv import load_dotenv
# import os

# load_dotenv()

# api_key = os.getenv("ANTHROPIC_API_KEY")

# if not api_key:
#     raise ValueError("ANTHROPIC_API_KEY not found")

# llm = ChatAnthropic(
#     model="claude-3-haiku-20240307",
#     temperature=0.3
# )

# response = llm.invoke("Hello Claude")

# print(response.content)