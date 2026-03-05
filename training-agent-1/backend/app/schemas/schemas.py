from pydantic import BaseModel

class TrainingRequest(BaseModel):
    level: str
    submission: str