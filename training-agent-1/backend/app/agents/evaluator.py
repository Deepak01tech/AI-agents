from config.llm import llm

def evaluate_submission(state):

    submission = state["submission"]

    prompt = f"""
    Evaluate this Python code and give a score out of 10.

    Code:
    {submission}
    """

    response = llm.invoke(prompt)

    state["evaluation"] = response.content
    return state