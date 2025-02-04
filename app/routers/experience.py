from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.schemas import ExperienceCreate, ExperienceResponse
from app.models import Experience
from app.database import get_db

router = APIRouter()


@router.get('/', response_model=list[ExperienceResponse])
def read_experience(db: Session = Depends(get_db)):
    """Fetch all profiles with their about paragraphs"""
    experience = db.query(Experience).all()
    return experience


@router.post('/', response_model=ExperienceResponse)
def create_experience(experience: ExperienceCreate, db: Session = Depends(get_db)):
    """Create a new profile with multiple about paragraphs"""
    experience_model = Experience(
        title=experience.title,
        date=experience.date,
        summary=experience.summary,
        tech=experience.tech,
        link=experience.link
    )

    db.add(experience_model)
    db.commit()
    db.refresh(experience_model)
    return experience_model


@router.put('/{experience_id}', response_model=ExperienceResponse)
def update_experience(experience_id: int, experience: ExperienceCreate, db: Session = Depends(get_db)):
    """Update a experience"""
    experience_model = db.query(Experience).filter(Experience.id == experience_id).first()

    if not experience_model:
        raise HTTPException(status_code=404, detail="Experience not found")

    experience_model.title = experience.title
    experience_model.date = experience.date
    experience_model.summary = experience.summary
    experience_model.tech = experience.tech
    experience_model.link = experience.link

    db.commit()
    db.refresh(experience_model)
    return experience_model


@router.delete('/{experience_id}')
def delete_experience(experience_id: int, db: Session = Depends(get_db)):
    """Delete a profile and its associated about paragraphs"""
    experience_model = db.query(Experience).filter(Experience.id == experience_id).first()

    if not experience_model:
        raise HTTPException(status_code=404, detail="Experience not found")

    db.delete(experience_model)
    db.commit()
    return {"message": "Experience deleted"}
