from config.llm import llm

def improvement_plan(state):

    gaps = state["skill_gaps"]

    prompt = f"""
    Suggest a learning improvement plan for these weaknesses:

    {gaps}
    """

    response = llm.invoke(prompt)

    state["plan"] = response.content
    return state