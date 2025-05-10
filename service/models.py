from pydantic import BaseModel, Field


class Plant(BaseModel):
    name: str
    image: str = Field(description="Image URL of the plant")
    description: str = Field(description="Description of the plant")
    care_instructions: str = Field(description="Care instructions for the plant")
    care_tips: str = Field(description="Care tips for the plant")
    AR_model: str = Field(description="AR model URL for the plant")


class Answer(BaseModel):
    description: str
    plants: list[Plant]
