from graph.training_graph import build_graph
from agents.topic_agent import assign_topic
# from graph.training_graph import build_graph

print("Building graph...")

graph = build_graph()

print("Running graph with test state...")

state = {
    "level": "beginner",
    "submission": """
def add(a,b):
 return a+b
"""
}

print("Invoking graph...")

result = graph.invoke(state)

print("Graph execution completed. Final report:")

print(result["report"])