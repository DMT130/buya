from fastapi import Depends, APIRouter, HTTPException, UploadFile, File
from query import crud_user_details as crud
from models import user_details_models as models
from schemas import user_details_schemas as schema
from database import SessionLocal, engine
from sqlalchemy.orm import Session
from typing import List
from api.api_auth_user import get_current_active_user, check_admin_rights, get_current_user
from schemas import user_schemas as schema_user
import shutil, os

#models.Base.metadata.create_all(bind=engine)
router = APIRouter()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/{user_id}/userdetails/", response_model=schema.UserDetails, tags=["User Details"])
def create_user_details(user_id:int, user_details: schema.UserDetailsCreate, db: Session = Depends(get_db),
                        current_user: schema_user.User=Depends(get_current_user)):
    return crud.create_user_details(db=db, user_details=user_details, user_id=user_id)


@router.get("/userdetails/", response_model=List[schema.UserDetails], tags=["User Details"])
def read_user_details(skip: int = 0, limit: int = 100, db: Session = Depends(get_db),
                      current_user: schema_user.User=Depends(get_current_user)):
    db_userdetails = crud.get_user_details(db, skip=skip, limit=limit)
    return db_userdetails

@router.get("/{userdetails_id}/userdetails/", response_model=schema.UserDetails, tags=["User Details"])
def read_user_details(userdetails_id: int, db: Session = Depends(get_db),
                      current_user: schema_user.User=Depends(get_current_user)):
    db_userdetails = crud.get_user_details_by_id(db, userdetails_id)
    if not db_userdetails:
        raise HTTPException(status_code=404, detail="userdetails not found")
    return db_userdetails

@router.patch("/{userdetails_id}/userdetails/", response_model=schema.UserDetails, tags=["User Details"])
def update_user_details(userdetails_id: int, userdetails_sch: schema.UserDetailsUpdate, db: Session = Depends(get_db),
                        current_user: schema_user.User=Depends(get_current_user)):
     db_userdetails = crud.get_user_details_by_id(db, userdetails_id)
     if not db_userdetails:
        raise HTTPException(status_code=404, detail="userdetails not found")
     result = crud.update_user_details(db, userdetails_sch, db_userdetails)
     return result

@router.delete("/{userdetails_id}/userdetails/", tags=["User Details"])
def delete_user_details(userdetails_id: int, db: Session = Depends(get_db),
                        current_user: schema_user.User=Depends(get_current_user)):
    db_userdetails = crud.get_user_details_by_id(db, userdetails_id)
    if not db_userdetails:
        raise HTTPException(status_code=404, detail="userdetails not found")
    result = crud.delete_user_details(db, db_userdetails)
    if result:
        raise HTTPException(status_code=200, detail="userdetails deleted")



#Role
@router.post("/role/", response_model=schema.Role, tags=["Role"])
def create_role(role: schema.RoleCreate, db: Session = Depends(get_db),
                current_user: schema_user.User=Depends(check_admin_rights)):
    return crud.create_role(db=db, role=role)


@router.get("/role/", response_model=List[schema.Role], tags=["Role"])
def read_role(skip: int = 0, limit: int = 100, db: Session = Depends(get_db),
              current_user: schema_user.User=Depends(check_admin_rights)):
    db_role = crud.get_role(db, skip=skip, limit=limit)
    return db_role

@router.get("/{role_id}/role/", response_model=schema.Role, tags=["Role"])
def read_role(role_id: int, db: Session = Depends(get_db), current_user: schema_user.User=Depends(check_admin_rights)):
    db_role = crud.get_role_by_id(db, role_id)
    if not db_role:
        raise HTTPException(status_code=404, detail="role not found")
    return db_role

@router.patch("/{role_id}/role/", response_model=schema.Role, tags=["Role"])
def update_role(role_id: int, role_sch: schema.RoleUpdate, db: Session = Depends(get_db), current_user: schema_user.User=Depends(check_admin_rights)):
     db_role = crud.get_role_by_id(db, role_id)
     if not db_role:
        raise HTTPException(status_code=404, detail="role not found")
     result = crud.update_role(db, role_sch, db_role)
     return result

@router.delete("/{role_id}/role/", tags=["Role"])
def delete_role(role_id: int, db: Session = Depends(get_db), current_user: schema_user.User=Depends(check_admin_rights)):
    db_role = crud.get_role_by_id(db, role_id)
    if not db_role:
        raise HTTPException(status_code=404, detail="role not found")
    result = crud.delete_role(db, db_role)
    if result:
        raise HTTPException(status_code=200, detail="role deleted")


#UserRole
@router.post("/{user_id}/{role_id}/userole/", response_model=schema.UserRole, tags=["User Role"])
def create_userole(user_id:int, role_id:int, userole: schema.UserRoleCreate, db: Session = Depends(get_db),
                   current_user: schema_user.User=Depends(check_admin_rights)):
    return crud.create_userole(db=db, userole=userole, user_id=user_id, role_id=role_id)


@router.get("/userole/", response_model=List[schema.UserRole], tags=["User Role"])
def read_userole(skip: int = 0, limit: int = 100, db: Session = Depends(get_db),
                 current_user: schema_user.User=Depends(check_admin_rights)):
    db_userole = crud.get_userole(db, skip=skip, limit=limit)
    return db_userole

@router.get("/{userole_id}/userole/", response_model=schema.UserRole, tags=["User Role"])
def read_userole(userole_id: int, db: Session = Depends(get_db),
                 current_user: schema_user.User=Depends(check_admin_rights)):
    db_userole = crud.get_userole_by_id(db, userole_id)
    if not db_userole:
        raise HTTPException(status_code=404, detail="userole not found")
    return db_userole

@router.patch("/{userole_id}/userole/", response_model=schema.UserRole, tags=["User Role"])
def update_userole(userole_id: int, userole_sch: schema.UserRoleUpdate, db: Session = Depends(get_db),
                   current_user: schema_user.User=Depends(check_admin_rights)):
     db_userole = crud.get_userole_by_id(db, userole_id)
     if not db_userole:
        raise HTTPException(status_code=404, detail="userole not found")
     result = crud.update_userole(db, userole_sch, db_userole)
     return result

@router.delete("/{userole_id}/userole/", tags=["User Role"])
def delete_userole(userole_id: int, db: Session = Depends(get_db), 
                   current_user: schema_user.User=Depends(check_admin_rights)):
    db_userole = crud.get_userole_by_id(db, userole_id)
    if not db_userole:
        raise HTTPException(status_code=404, detail="userole not found")
    result = crud.delete_userole(db, db_userole)
    if result:
        raise HTTPException(status_code=200, detail="userole deleted")
    



#Asset Images
@router.post("/profile-picture/", tags=["Profile Picture"])
def create_upload_files(user_id: int, file: UploadFile = File(...), db: Session = Depends(get_db)):
    filename = file.filename
    file_path = os.path.join("ProfilePicture", filename)
    with open(file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)
    image = models.ProfilePicture(user_id=user_id, name=filename, path=file_path, type=file.content_type)
    db.add(image)
    db.commit()
    db.refresh(image)
    return {"image_url": file_path}

#update Images
@router.put("/profile-picture/{image_id}", tags=["Profile Picture"])
def update_image(image_id: int, image: schema.ProfilePictureUpdate, db: Session = Depends(get_db)):
    db_image = db.query(models.ProfilePicture).filter(models.ProfilePicture.id == image_id).first()
    if not db_image:
        raise HTTPException(status_code=404, detail="Image not found")
    for field, value in image.dict(exclude_unset=True).items():
        setattr(db_image, field, value)
    db.commit()
    db.refresh(db_image)
    return db_image

#delete Images
@router.delete("/profile-picture/{image_id}", tags=["Profile Picture"])
def delete_image(image_id: int, db: Session = Depends(get_db)):
    db_image = db.query(models.ProfilePicture).filter(models.ProfilePicture.id == image_id).first()
    if not db_image:
        raise HTTPException(status_code=404, detail="Image not found")
    db.delete(db_image)
    db.commit()
    return {"message": "Image deleted successfully"}

#Real all Images
@router.get("/profile-picture/", response_model=List[schema.ProfilePicture], tags=["Profile Picture"])
def read_images(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    images = db.query(models.ProfilePicture).offset(skip).limit(limit).all()
    return images

#Real one Images
@router.get("/profile-picture/{image_id}", response_model=schema.ProfilePicture, tags=["Profile Picture"])
def read_one_image(image_id: int, db: Session = Depends(get_db)):
    images = db.query(models.ProfilePicture).filter(models.ProfilePicture.id == image_id).first()
    return images

#Real one Asset_id
@router.get("/profile-picture/{user_id}", response_model=schema.ProfilePicture, tags=["Profile Picture"])
def read_image_by_asset(user_id: int, db: Session = Depends(get_db)):
    images = db.query(models.ProfilePicture).filter(models.ProfilePicture.user_id == user_id).all()
    return images