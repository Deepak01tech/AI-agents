from config.llm import llm

def generate_task(state):

    topic = state["topic"]

    prompt = f"""
    Create 3 coding tasks for learning {topic}.
    """

    response = llm.invoke(prompt)

    state["tasks"] = response.content
    return state