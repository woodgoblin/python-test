from sqlalchemy.orm import Session
from app.models import Cat, Rat
from app.schemas import CatCreate, RatCreate


# CRUD for Cats
def get_cats(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Cat).offset(skip).limit(limit).all()


def get_cat(db: Session, cat_id: int):
    return db.query(Cat).filter(Cat.id == cat_id).first()


def create_cat(db: Session, cat: CatCreate):
    db_cat = Cat(**cat.dict())
    db.add(db_cat)
    db.commit()
    db.refresh(db_cat)
    return db_cat


def update_cat(db: Session, cat_id: int, cat: CatCreate):
    db_cat = get_cat(db, cat_id)
    if db_cat:
        for key, value in cat.dict().items():
            setattr(db_cat, key, value)
        db.commit()
        db.refresh(db_cat)
    return db_cat


def delete_cat(db: Session, cat_id: int):
    db_cat = get_cat(db, cat_id)
    if db_cat:
        db.delete(db_cat)
        db.commit()
    return db_cat


# CRUD for Rats
def get_rats(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Rat).offset(skip).limit(limit).all()


def get_rat(db: Session, rat_id: int):
    return db.query(Rat).filter(Rat.ID == rat_id).first()


def create_rat(db: Session, rat: RatCreate):
    db_rat = Rat(**rat.dict())
    db.add(db_rat)
    db.commit()
    db.refresh(db_rat)
    return db_rat


def update_rat(db: Session, rat_id: int, rat: RatCreate):
    db_rat = get_rat(db, rat_id)
    if db_rat:
        for key, value in rat.dict().items():
            setattr(db_rat, key, value)
        db.commit()
        db.refresh(db_rat)
    return db_rat


def delete_rat(db: Session, rat_id: int):
    db_rat = get_rat(db, rat_id)
    if db_rat:
        db.delete(db_rat)
        db.commit()
    return db_rat
