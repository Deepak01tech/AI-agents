from config.llm import llm

def generate_project(state):

    topic = state["topic"]

    prompt = f"""
    Create a mini Python project based on {topic}.
    """

    response = llm.invoke(prompt)

    state["project"] = response.content
    return state