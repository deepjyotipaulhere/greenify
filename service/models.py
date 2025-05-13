from pydantic import BaseModel, Field


class Plant(BaseModel):
    name: str
    image: str = Field(description="Image URL of the plant")
    description: str = Field(description="Description of the plant")
    care_instructions: str = Field(description="Care instructions for the plant")
    care_tips: str = Field(description="Care tips for the plant")
    AR_model: str = Field(description="AR model URL for the plant")


class Answer1(BaseModel):
    description: str

class Answer2(BaseModel):
    plants: list[Plant]


class Benefit(BaseModel):
    type: str = Field(description="Type of the environmental benefit")
    amount: str = Field(description="How much percentage of improvement")
    direction: bool = Field(description="True means increasing, False means decreasing")


class Group(BaseModel):
    users: list[str] = Field(
        description="List at least 2 or more users with similar plant suggestions and how they can combine same job in term of place, activities and plantation"
    )
    description: list[str] = Field(
        description="Short description of how these people match with each other"
    )
    benefits: list[Benefit] = Field(
        description="How this combination helps benefit the environment with parameter, percentage value"
    )


class Community(BaseModel):
    match: list[Group]
