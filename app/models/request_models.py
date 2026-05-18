from pydantic import BaseModel

class RecommendRequest(BaseModel):
    prompt: str
