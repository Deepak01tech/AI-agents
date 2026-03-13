import os
import sys
import subprocess
import traceback
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))

# ---------------------------------------------------------------------------
# Tool Definitions — Decorated with @tool for LangChain/LangGraph
# ---------------------------------------------------------------------------

@tool
def run_python_code(code: str) -> str:
    """Execute a Python code snippet and return stdout and stderr output.
    Use this tool when you need to run, test, or verify Python code.
    The code runs in a subprocess with a 15-second timeout.
    
    Args:
        code: The Python source code to execute.
    
    Returns:
        A string containing the combined stdout and stderr output.
    """
    try:
        result = subprocess.run(
            [sys.executable, "-c", code],
            capture_output=True,
            text=True,
            timeout=15,
            cwd=os.path.dirname(__file__),
        )
        output = ""
        if result.stdout:
            output += result.stdout
        if result.stderr:
            output += ("\n[stderr]\n" + result.stderr) if output else result.stderr
        return output.strip() if output.strip() else "(Code executed successfully with no output)"
    except subprocess.TimeoutExpired:
        return "Error: Code execution timed out (15 second limit)."
    except Exception as e:
        return f"Error executing code: {str(e)}"


@tool
def web_search(query: str) -> str:
    """Search the web for current information using DuckDuckGo.
    Use this tool when you need up-to-date information, documentation links,
    or facts that may have changed after your training data cutoff.
    
    Args:
        query: The search query string.
    
    Returns:
        A string containing the top search results with titles, URLs, and snippets.
    """
    try:
        from duckduckgo_search import DDGS
        results = DDGS().text(query, max_results=5)
        if not results:
            return "No search results found."
        
        formatted = []
        for r in results:
            formatted.append(f"**{r['title']}**\n{r['href']}\n{r['body']}\n")
        return "\n".join(formatted)
    except ImportError:
        return "Error: duckduckgo-search package is not installed."
    except Exception as e:
        return f"Search error: {str(e)}"


# ---------------------------------------------------------------------------
# System Prompt
# ---------------------------------------------------------------------------

SYSTEM_INSTRUCTION = """You are Bridgefix AI, an expert AI coding assistant with real capabilities.

You have access to the following tools:
1. **run_python_code** — Execute Python code to verify solutions, perform calculations, test logic, or demonstrate output.
2. **web_search** — Search the web for current documentation, latest versions, error solutions, or any up-to-date information.

Guidelines:
- When the user asks you to run or test code, USE the run_python_code tool. Don't just show code — actually execute it.
- When the user asks about current events, latest versions, or needs up-to-date info, USE the web_search tool.
- You can chain multiple tool calls: e.g., search for info, then write and run code based on it.
- Always explain what you did and show the results clearly.
- Provide concise explanations and well-formatted code blocks with language labels.
- If code execution fails, analyze the error and suggest fixes.
- You remember the full conversation history within a session."""


# ---------------------------------------------------------------------------
# LangGraph Agent Setup
# ---------------------------------------------------------------------------

# Initialize the LLM
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0.2,
    google_api_key=os.getenv("GEMINI_API_KEY"),
)

# Tools list
tools = [run_python_code, web_search]

# Memory checkpointer — stores conversation history per thread_id
memory = MemorySaver()

# Create the ReAct agent graph
# This builds a graph: Agent Node → (decides) → Tool Node → (result) → Agent Node → ...
agent = create_react_agent(
    model=llm,
    tools=tools,
    checkpointer=memory,
    prompt=SYSTEM_INSTRUCTION,
)


# ---------------------------------------------------------------------------
# Public API — called by main.py
# ---------------------------------------------------------------------------

def process_message(message: str, session_id: str = "default") -> dict:
    """
    Process a user message within a LangGraph session. Returns a dict with:
      - response: the AI's text response
      - tools_used: list of tool names invoked during this turn
      - error: error string if something went wrong (else None)
    """
    try:
        # LangGraph uses thread_id for conversation memory
        config = {"configurable": {"thread_id": session_id}}

        # Invoke the agent graph
        result = agent.invoke(
            {"messages": [HumanMessage(content=message)]},
            config=config,
        )

        # Extract the final AI response (last message)
        messages = result.get("messages", [])
        response_text = ""
        tools_used = set()

        for msg in messages:
            # Collect tool calls from AI messages
            if hasattr(msg, 'tool_calls') and msg.tool_calls:
                for tc in msg.tool_calls:
                    tools_used.add(tc.get("name", "unknown"))
            
            # Also check message type for tool messages
            if msg.type == "tool":
                # The tool message's name attribute tells us which tool was called
                if hasattr(msg, 'name') and msg.name:
                    tools_used.add(msg.name)

        # The last AI message is our response
        if messages:
            last_msg = messages[-1]

            if hasattr(last_msg, "content"):
                content = last_msg.content

                # If content is a list (LangGraph format), extract text
                if isinstance(content, list):
                    parts = []
                    for item in content:
                        if isinstance(item, dict) and "text" in item:
                            parts.append(item["text"])
                        else:
                            parts.append(str(item))
                    response_text = " ".join(parts)
                else:
                    response_text = str(content)
            else:
                response_text = str(last_msg)

        return {
            "response": response_text or "No response generated.",
            "tools_used": list(tools_used),
            "error": None,
        }

    except Exception as e:
        traceback.print_exc()
        return {
            "response": "",
            "tools_used": [],
            "error": f"Agent Error: {str(e)}",
        }


def clear_session(session_id: str = "default") -> bool:
    """Clear a chat session by removing its memory checkpoint."""
    global agent, memory
    try:
        # Recreate the memory saver to clear all checkpoints
        # (MemorySaver stores in-memory, so we replace it)
        memory = MemorySaver()
        agent = create_react_agent(
            model=llm,
            tools=tools,
            checkpointer=memory,
            prompt=SYSTEM_INSTRUCTION,
        )
        return True
    except Exception:
        traceback.print_exc()
        return False


# ---------------------------------------------------------------------------
# CLI mode for quick testing
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print("Bridgefix AI Agent (LangGraph) — CLI Mode (type 'exit' to quit)\n")
    sid = "cli"
    while True:
        user_input = input("\nYou: ")
        if user_input.lower() in ["exit", "quit"]:
            break
        result = process_message(user_input, session_id=sid)
        if result["tools_used"]:
            print(f"\n🔧 Tools used: {', '.join(result['tools_used'])}")
        if result["error"]:
            print(f"\n❌ Error: {result['error']}")
        else:
            print(f"\nAssistant: {result['response']}")