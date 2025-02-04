from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.schemas import ProfileCreate, ProfileResponse, AboutParagraphCreate
from app.models import Profile, AboutParagraph
from app.database import get_db

router = APIRouter()


@router.get('/', response_model=list[ProfileResponse])
def read_profiles(db: Session = Depends(get_db)):
    """Fetch all profiles with their about paragraphs"""
    profiles = db.query(Profile).all()
    return profiles


@router.post('/', response_model=ProfileResponse)
def create_profile(profile: ProfileCreate, db: Session = Depends(get_db)):
    """Create a new profile with multiple about paragraphs"""
    profile_model = Profile(
        name=profile.name,
        position=profile.position,
        summary=profile.summary
    )

    # Add related about paragraphs
    for paragraph in profile.about_paragraphs:
        profile_model.about_paragraphs.append(AboutParagraph(text=paragraph.text))

    db.add(profile_model)
    db.commit()
    db.refresh(profile_model)
    return profile_model


@router.put('/{profile_id}', response_model=ProfileResponse)
def update_profile(profile_id: int, profile: ProfileCreate, db: Session = Depends(get_db)):
    """Update a profile and replace its about paragraphs"""
    profile_model = db.query(Profile).filter(Profile.id == profile_id).first()

    if not profile_model:
        raise HTTPException(status_code=404, detail="Profile not found")

    profile_model.name = profile.name
    profile_model.position = profile.position
    profile_model.summary = profile.summary

    # Clear existing about paragraphs and replace them
    db.query(AboutParagraph).filter(AboutParagraph.profile_id == profile_id).delete()
    for paragraph in profile.about_paragraphs:
        profile_model.about_paragraphs.append(AboutParagraph(text=paragraph.text))

    db.commit()
    db.refresh(profile_model)
    return profile_model


@router.delete('/{profile_id}')
def delete_profile(profile_id: int, db: Session = Depends(get_db)):
    """Delete a profile and its associated about paragraphs"""
    profile_model = db.query(Profile).filter(Profile.id == profile_id).first()

    if not profile_model:
        raise HTTPException(status_code=404, detail="Profile not found")

    db.delete(profile_model)
    db.commit()
    return {"message": "Profile deleted"}
