from langgraph.graph import StateGraph, END

from agents.topic_agent import assign_topic
from agents.task_generator import generate_task
from agents.project_generator import generate_project
from agents.evaluator import evaluate_submission
from agents.skill_analyzer import analyze_skills
from agents.improvement_planner import improvement_plan
from agents.report_generator import generate_report
# from agents.topic_agent import assign_topic


def build_graph():

    workflow = StateGraph(dict)

    workflow.add_node("topic", assign_topic)
    workflow.add_node("task", generate_task)
    workflow.add_node("project", generate_project)
    workflow.add_node("evaluate", evaluate_submission)
    workflow.add_node("analyze", analyze_skills)
    workflow.add_node("plan", improvement_plan)
    workflow.add_node("report", generate_report)

    workflow.set_entry_point("topic")

    workflow.add_edge("topic", "task")
    workflow.add_edge("task", "project")
    workflow.add_edge("project", "evaluate")
    workflow.add_edge("evaluate", "analyze")
    workflow.add_edge("analyze", "plan")
    workflow.add_edge("plan", "report")
    workflow.add_edge("report", END)

    return workflow.compile()