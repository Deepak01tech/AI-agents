# Refactor Agent to Use LangGraph

Replace the native Gemini SDK function calling with **LangGraph** for a proper graph-based agent architecture with persistent memory, conditional routing, and extensibility.

## Proposed Changes

### Backend: Dependencies

---

#### [MODIFY] [requirements.txt](file:///c:/Users/deepe/Desktop/Dp/AI-agents/AI%20coding%20Assistant%20web%20app/backend/requirements.txt)

Replace `google-genai` with LangChain/LangGraph packages:

```diff
-google-genai==1.2.0
+langchain-google-genai>=2.1.0
+langgraph>=0.4.0
+langchain-core>=0.3.0
```

Keep: `fastapi`, `uvicorn`, `pydantic`, `python-dotenv`, `duckduckgo-search`

---

### Backend: Agent Core

---

#### [MODIFY] [agent.py](file:///c:/Users/deepe/Desktop/Dp/AI-agents/AI%20coding%20Assistant%20web%20app/backend/agent.py)

Full rewrite using LangGraph's `create_react_agent`:

**Key components:**
1. **`ChatGoogleGenerativeAI`** — LangChain wrapper for Gemini, replaces the raw `google-genai` client
2. **`@tool` decorated functions** — Same [run_python_code](file:///c:/Users/deepe/Desktop/Dp/AI-agents/AI%20coding%20Assistant%20web%20app/backend/agent.py#18-47) and [web_search](file:///c:/Users/deepe/Desktop/Dp/AI-agents/AI%20coding%20Assistant%20web%20app/backend/agent.py#49-74) tools, now using LangChain's `@tool` decorator
3. **`create_react_agent()`** — LangGraph's pre-built ReAct agent that handles the think→act→observe loop as a state graph
4. **`MemorySaver`** — LangGraph's checkpointer for conversation memory, with `thread_id` mapping to session IDs

```python
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.tools import tool

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.2)
memory = MemorySaver()
agent = create_react_agent(llm, tools=[run_python_code, web_search], checkpointer=memory)
```

**Architecture diagram:**
```
User Message → [Agent Node] → decides → [Tool Node] → executes → [Agent Node] → responds
                    ↑                                                    |
                    └────────── loops if more tools needed ──────────────┘
```

---

#### [MODIFY] [main.py](file:///c:/Users/deepe/Desktop/Dp/AI-agents/AI%20coding%20Assistant%20web%20app/backend/main.py)

- Minor: Update imports from [agent.py](file:///c:/Users/deepe/Desktop/Dp/AI-agents/AI%20coding%20Assistant%20web%20app/backend/agent.py) (function signatures stay the same)
- No other changes needed — the API contract remains identical

---

### Frontend

**No changes needed** — The frontend API contract (`session_id`, `tools_used`, `response`) stays identical.

---

## What This Gets You (vs. Current)

| Feature | Current (Gemini Native) | After (LangGraph) |
|---|---|---|
| Agent loop | SDK auto-function-calling | Explicit graph: Agent → Tool → Agent |
| Memory | In-memory dict of Chat objects | `MemorySaver` (upgradeable to SQLite/Postgres) |
| Extensibility | Limited | Add nodes, edges, conditional branches |
| Debugging | Opaque SDK internals | Full graph state inspection |
| Multi-agent | Not possible | Supervisor/swarm patterns ready |

## Verification Plan

### Automated
- `npm run build` — frontend compilation check
- `pip install` new deps — no conflicts

### Manual
1. **Memory**: "My name is Deepak" → "What's my name?" → should remember
2. **Code execution**: "Run `print(2+2)`" → should return `4`
3. **Web search**: "Latest Python version" → should search and respond
4. **New session**: Click "New session" → memory should be cleared
