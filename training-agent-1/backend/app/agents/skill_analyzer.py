from config.llm import llm

def analyze_skills(state):

    evaluation = state["evaluation"]

    prompt = f"""
    Based on this evaluation identify weak areas.

    {evaluation}
    """

    response = llm.invoke(prompt)

    state["skill_gaps"] = response.content
    return state