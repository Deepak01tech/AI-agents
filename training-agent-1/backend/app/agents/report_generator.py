def generate_report(state):

    report = f"""
    Weekly Topic: {state['topic']}

    Tasks:
    {state['tasks']}

    Evaluation:
    {state['evaluation']}

    Skill Gaps:
    {state['skill_gaps']}

    Improvement Plan:
    {state['plan']}
    """

    state["report"] = report

    return state