from fastapi import APIRouter
from schemas.schemas import TrainingRequest
from graph.training_graph import build_graph

router = APIRouter()

graph = build_graph()

@router.post("/train")

def run_training(data: TrainingRequest):

    state = {
        "level": data.level,
        "submission": data.submission
    }

    result = graph.invoke(state)

    return {
        "topic": result["topic"],
        "tasks": result["tasks"],
        "project": result["project"],
        "evaluation": result["evaluation"],
        "plan": result["plan"],
        "report": result["report"]
    }