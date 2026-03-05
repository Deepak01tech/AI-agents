from config.llm import llm

def assign_topic(state):

    level = state.get("level", "beginner")

    prompt = f"""
    Suggest a Python learning topic for a {level} developer for this week.
    """

    response = llm.invoke(prompt)

    state["topic"] = response.content
    return state