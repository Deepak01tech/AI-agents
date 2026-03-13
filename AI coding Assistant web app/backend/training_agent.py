from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from training_state import AgentState
from training_nodes import planner_node, task_generator_node, evaluator_node, reporter_node
from langchain_core.messages import HumanMessage, SystemMessage

# ---------------------------------------------------------------------------
# Graph Construction
# ---------------------------------------------------------------------------

def create_training_graph():
    builder = StateGraph(AgentState)
    
    # Add nodes
    builder.add_node("planner", planner_node)
    builder.add_node("task_generator", task_generator_node)
    builder.add_node("evaluator", evaluator_node)
    builder.add_node("reporter", reporter_node)
    
    # Starting routing: START -> Node based on state
    def route_start(state: AgentState):
        last_message = state['messages'][-1].content.lower() if state['messages'] else ""
        
        # Check for submission
        if "```" in last_message or "def " in last_message:
            return "evaluator"
        
        # Check for report
        if "report" in last_message or "progress" in last_message:
            return "reporter"
            
        # Decision based on state
        if state['current_topic'] is None:
            return "planner"
        if state['active_task'] is None:
            return "task_generator"
            
        return "planner" # Default/Fallback

    builder.add_conditional_edges(START, route_start)
    
    # Standard edges
    builder.add_edge("planner", "task_generator")
    builder.add_edge("task_generator", END)
    builder.add_edge("evaluator", END)
    builder.add_edge("reporter", END)
    
    # Build with checkpointer
    memory = MemorySaver()
    return builder.compile(checkpointer=memory)

# Pre-compiled graph instance
training_agent = create_training_graph()

# ---------------------------------------------------------------------------
# Initial State Factory
# ---------------------------------------------------------------------------

def get_initial_training_state() -> dict:
    return {
        "messages": [],
        "developer_level": "Beginner",
        "completed_topics": [],
        "current_week": 1,
        "current_topic": None,
        "active_task": None,
        "performance_metrics": {
            "exercises_completed": 0,
            "projects_completed": 0,
            "average_score": 0.0,
            "common_errors": [],
            "strengths": [],
            "weaknesses": []
        },
        "last_evaluation_feedback": None,
        "last_evaluation_score": None,
        "is_ready_for_next_task": True,
        "requires_improvement_plan": False
    }

# ---------------------------------------------------------------------------
# Execution Wrapper
# ---------------------------------------------------------------------------

def process_training_message(message: str, session_id: str = "training_default"):
    """Entry point for the backend API."""
    config = {"configurable": {"thread_id": session_id}}
    
    # Check if we have an existing state, if not, we can initialize it
    # But LangGraph's invoke will create the state based on START conditional edge
    
    try:
        # Run the graph. The route_start conditional edge from START 
        # will decide which node to visit first.
        result = training_agent.invoke(
            {"messages": [HumanMessage(content=message)]},
            config=config
        )
        
        # Extract last AI message
        last_msg = result["messages"][-1]
        
        return {
            "response": last_msg.content,
            "state": {
                "week": result["current_week"],
                "topic": result["current_topic"],
                "active_task": result["active_task"],
                "metrics": result["performance_metrics"]
            },
            "error": None
        }
    except Exception as e:
        import traceback
        traceback.print_exc()
        return {
            "response": "I encountered an error while processing your training request.",
            "state": None,
            "error": str(e)
        }
