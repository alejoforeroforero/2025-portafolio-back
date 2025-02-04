from pydantic import BaseModel, Field
from typing import List
from typing import Optional

# Schema for the AboutParagraph table
class AboutParagraphBase(BaseModel):
    text: str

class AboutParagraphCreate(AboutParagraphBase):
    pass

class AboutParagraphResponse(AboutParagraphBase):
    id: int
    profile_id: int

    class Config:
        from_attributes = True  # Enables ORM mode

# Schema for Profile
class ProfileBase(BaseModel):
    name: str
    position: str
    summary: str

class ProfileCreate(ProfileBase):
    about_paragraphs: List[AboutParagraphCreate] = []  # Accepts a list of about paragraphs

class ProfileResponse(ProfileBase):
    id: int
    about_paragraphs: List[AboutParagraphResponse] = []  # Returns related about paragraphs

    class Config:
        from_attributes = True

# Schema for Experience
class ExperienceCreate(BaseModel):
    title: str
    date: str
    summary: str
    tech: str
    link:str

class ExperienceResponse(BaseModel):
    id: int
    title: str
    date: str
    summary: str
    tech: str
    link: Optional[str] = Field(default="")  

    class Config:
        from_attributes = True
