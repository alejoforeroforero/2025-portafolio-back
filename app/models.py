from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base  # Assuming you have a Base class for SQLAlchemy models

class Profile(Base):
    __tablename__ = "profiles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    position = Column(String)
    summary = Column(String)
    about_paragraphs = relationship("AboutParagraph", back_populates="profile", cascade="all, delete-orphan")

class AboutParagraph(Base):
    __tablename__ = "about_paragraphs"

    id = Column(Integer, primary_key=True, index=True)
    profile_id = Column(Integer, ForeignKey("profiles.id", ondelete="CASCADE"))
    text = Column(String, nullable=False)

    profile = relationship("Profile", back_populates="about_paragraphs")

class Experience(Base):
    __tablename__ = "experience"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    date = Column(String)
    summary = Column(String)
    tech = Column(String)
    link = Column(String)
