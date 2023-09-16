from pydantic import BaseModel, EmailStr, Field


class User(BaseModel):
    name: str = Field(
        min_length=3,
        max_length=50,
        title="Name",
        description="Name of the user",
        examples=["name"],
    )
    email: EmailStr = Field(
        title="Email", description="Email of the user", examples=["test@gmail.com"]
    )
    password: str = Field(
        default="password",
        min_length=3,
        max_length=80,
        title="Password",
        description="Password of the user",
        examples=["password"],
    )
