from typing import Annotated, List, TypedDict, Dict, Any, Optional
from langchain_core.messages import BaseMessage
import operator

class PerformanceMetrics(TypedDict):
    exercises_completed: int
    projects_completed: int
    average_score: float
    common_errors: List[str]
    strengths: List[str]
    weaknesses: List[str]

class Task(TypedDict):
    id: str
    type: str # "exercise" or "project"
    title: str
    description: str
    requirements: List[str]
    learning_objectives: List[str]
    difficulty: str # "Easy", "Medium", "Hard"
    starter_code: Optional[str]

class AgentState(TypedDict):
    # messages is a list of BaseMessage, and we use Annotated with operator.add
    # to indicate that new messages should be appended to the list.
    messages: Annotated[List[BaseMessage], operator.add]
    
    # Trainee Profile
    developer_level: str # "Beginner", "Intermediate", "Advanced"
    completed_topics: List[str]
    
    # Progress Tracking
    current_week: int
    current_topic: Optional[str]
    active_task: Optional[Task]
    
    # Performance
    performance_metrics: PerformanceMetrics
    
    # Evaluation Results
    last_evaluation_feedback: Optional[str]
    last_evaluation_score: Optional[int] # 0-100
    
    # System Flags
    is_ready_for_next_task: bool
    requires_improvement_plan: bool
