# Project Walkthrough: AI Coding Assistant & Training Agent

## 1. Multi-Capability AI Agent
The core application is now a sophisticated AI Agent built on **LangGraph**. It goes beyond simple chat by using tools and memory.

### Features
- **Conversation Memory**: Persists history across messages using LangGraph checkpoints.
- **Code Execution**: Runs Python code snippets in a safe subprocess.
- **Web Search**: Retrieves current information via DuckDuckGo.
- **Multi-step Reasoning**: Automatically chains tools (e.g., Search -> Code -> Reply).

---

## 2. Python Training Agent (New!)
A specialized system designed to guide junior developers through a Python curriculum.

### Features
- **Weekly Curriculum**: Automatically assigns learning topics (OOP, Decorators, etc.) based on progress.
- **Task Generation**: Creates level-appropriate coding exercises and mini-projects.
- **Automated Evaluation**: Grades submissions, provides constructive feedback, and tracks scores.
- **Performance tracking**: Monitors strengths, weaknesses, and common errors over time.
- **Progress Reports**: Generates detailed summaries and personalized improvement plans.

### Training Backend Architecture
The Training Agent is a **state-based graph** with specialized nodes:
- `Planner`: Decides the curriculum.
- `Task Generator`: Creates the content.
- `Evaluator`: Reviews the work.
- `Reporter`: Analyzes the data.

---

## 3. Technical Implementation

### Key Files
- [agent.py](file:///c:/Users/deepe/Desktop/Dp/AI-agents/AI%20coding%20Assistant%20web%20app/backend/agent.py): LangGraph implementation for the general assistant.
- [training_agent.py](file:///c:/Users/deepe/Desktop/Dp/AI-agents/AI%20coding%20Assistant%20web%20app/backend/training_agent.py): LangGraph implementation for the training curriculum.
- [training_nodes.py](file:///c:/Users/deepe/Desktop/Dp/AI-agents/AI%20coding%20Assistant%20web%20app/backend/training_nodes.py): Specialized logic for planner, generator, evaluator.
- [training_state.py](file:///c:/Users/deepe/Desktop/Dp/AI-agents/AI%20coding%20Assistant%20web%20app/backend/training_state.py): TypedDict defining the complex state of a trainee.
- [main.py](file:///c:/Users/deepe/Desktop/Dp/AI-agents/AI%20coding%20Assistant%20web%20app/backend/main.py): FastAPI endpoints for both agents.

### Verification
- ✅ **Backend Integration**: All endpoints (`/api/chat`, `/api/training/chat`, etc.) are exposed.
- ✅ **Graph Routing**: Conditional routing logic tested and implemented.
- ✅ **State Persistence**: Memory enabled via `MemorySaver`.

---

## Next Steps
- **Frontend Dashboard**: Building a dedicated UI for the Training Agent to show progress bars, active tasks, and performance charts.
- **Persistent DB**: Upgrading from in-memory checkpoints to SQLite for permanent data storage.
