import os
from typing import List, Optional
from pydantic import BaseModel, Field
from langchain_google_genai import ChatGoogleGenerativeAI
# from langchain_core.messages import AISameMessage, HumanMessage, SystemMessage
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

from training_state import AgentState, Task, PerformanceMetrics

# Initialize LLM
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.2,
    google_api_key=os.getenv("GEMINI_API_KEY"),
)

# ---------------------------------------------------------------------------
# Structured Output Models
# ---------------------------------------------------------------------------

class PlannedTopic(BaseModel):
    topic: str = Field(description="The learning topic for the week")
    objectives: List[str] = Field(description="List of learning objectives")
    explanation: str = Field(description="A brief explanation of the topic for the junior developer")

class GeneratedTask(BaseModel):
    title: str = Field(description="Title of the task")
    type: str = Field(description="'exercise' or 'project'")
    description: str = Field(description="Detailed instructions")
    requirements: List[str] = Field(description="Specific technical requirements or constraints")
    starter_code: Optional[str] = Field(description="Boilerplate code if needed")
    difficulty: str = Field(description="'Easy', 'Medium', or 'Hard'")

class EvaluationResult(BaseModel):
    score: int = Field(description="Score from 0-100")
    feedback: str = Field(description="Detailed constructive feedback")
    is_ready_for_next: bool = Field(description="Whether the trainee has mastered the topic and can move on")
    detected_strengths: List[str] = Field(description="Concepts the trainee showed mastery in")
    detected_weaknesses: List[str] = Field(description="Concepts the trainee struggled with")

# ---------------------------------------------------------------------------
# Node Implementations
# ---------------------------------------------------------------------------

def planner_node(state: AgentState):
    """Assigns the next learning topic based on progress."""
    planner_llm = llm.with_structured_output(PlannedTopic)
    
    prompt = f"""You are a Python curriculum expert. 
    Developer Level: {state['developer_level']}
    Completed Topics: {', '.join(state['completed_topics'])}
    Current Week: {state['current_week']}
    
    Suggest the next most logical topic for a junior Python developer. 
    Stay focused on core Python, data structures, and best practices.
    """
    
    result = planner_llm.invoke([SystemMessage(content=prompt)])
    
    return {
        "current_topic": result.topic,
        "messages": [AISameMessage(content=f"Planning for Week {state['current_week']}: {result.topic}\n\n{result.explanation}")]
    }

def task_generator_node(state: AgentState):
    """Generates an exercise or project for the current topic."""
    task_llm = llm.with_structured_output(GeneratedTask)
    
    prompt = f"""Generate a coding task for the topic: {state['current_topic']}
    Developer Level: {state['developer_level']}
    Performance context: Target {state['developer_level']} level constraints.
    
    Provide a title, description, requirements, and optional starter code.
    """
    
    result = task_llm.invoke([SystemMessage(content=prompt)])
    
    # Create the task object for the state
    new_task = Task(
        id=f"w{state['current_week']}_{result.type}",
        type=result.type,
        title=result.title,
        description=result.description,
        requirements=result.requirements,
        learning_objectives=[], # Simplified for now
        difficulty=result.difficulty,
        starter_code=result.starter_code
    )
    
    return {
        "active_task": new_task,
        "messages": [AISameMessage(content=f"Your task for this topic: **{result.title}**\n\n{result.description}")]
    }

def evaluator_node(state: AgentState):
    """Evaluates user code submission."""
    # Note: In a real implementation, this node would first call the 'run_python_code' tool
    # For now, we simulate the LLM evaluation of the code in the messages
    
    evaluator_llm = llm.with_structured_output(EvaluationResult)
    
    # Get the last user message (presumably containing the code)
    user_submission = state['messages'][-1].content
    
    prompt = f"""Evaluate the following Python submission for the task: {state['active_task']['title']}
    Requirements: {', '.join(state['active_task']['requirements'])}
    
    Submission:
    {user_submission}
    
    Provide a score, feedback, and analyze strengths/weaknesses.
    """
    
    result = evaluator_llm.invoke([SystemMessage(content=prompt)])
    
    # Update performance metrics logic (simplified)
    new_metrics = state['performance_metrics'].copy()
    if state['active_task']['type'] == "exercise":
        new_metrics['exercises_completed'] += 1
    else:
        new_metrics['projects_completed'] += 1
    
    # Average score update
    total_completed = new_metrics['exercises_completed'] + new_metrics['projects_completed']
    new_metrics['average_score'] = ((new_metrics['average_score'] * (total_completed - 1)) + result.score) / total_completed
    
    # Append unique strengths/weaknesses
    new_metrics['strengths'] = list(set(new_metrics['strengths'] + result.detected_strengths))
    new_metrics['weaknesses'] = list(set(new_metrics['weaknesses'] + result.detected_weaknesses))
    
    updates = {
        "last_evaluation_score": result.score,
        "last_evaluation_feedback": result.feedback,
        "performance_metrics": new_metrics,
        "is_ready_for_next_task": result.is_ready_for_next,
        "messages": [AISameMessage(content=f"#### Evaluation Result: {result.score}/100\n\n{result.feedback}")]
    }
    
    # If mastered, move topic to completed and increment week
    if result.is_ready_for_next:
        updates["completed_topics"] = state['completed_topics'] + [state['current_topic']]
        updates["current_week"] = state['current_week'] + 1
        updates["active_task"] = None
        
    return updates

def reporter_node(state: AgentState):
    """Generates a progress report and improvement plan."""
    prompt = f"""Generate a comprehensive progress report for a junior developer.
    Level: {state['developer_level']}
    Week: {state['current_week']}
    Metric: {state['performance_metrics']}
    Completed Topics: {state['completed_topics']}
    
    Summarize their journey, suggest a personalized improvement plan, and encourage them.
    """
    
    response = llm.invoke([SystemMessage(content=prompt)])
    
    return {
        "messages": [AISameMessage(content=f"### 📊 Progress Report\n\n{response.content}")]
    }
