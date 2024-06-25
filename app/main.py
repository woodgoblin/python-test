from typing import List

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import SessionLocal, engine, Base
from app.schemas import CatCreate, Cat, RatCreate, Rat
from app import crud

Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Cat endpoints
@app.post("/cats/", response_model=Cat, responses={
    200: {
        "description": "Cat created successfully",
        "content": {
            "application/json": {
                "example": {
                    "MY CAT": "MY CAT MY CAT IS ON FIRE",
                    "WE DON'T NEED NO WATER LET THE ": "<HERE GOES NON-PC>",
                    "<NON PC>": "<MORE NON PC> <NON PC>",
                    "OBVIOUSLY BLOODHOUND": "GANG DOESN'T ",
                    "NEED TO GIVE A SHOW IN MY SWAGGER": "OH YEAH IT DOES NOT",
                    "BUT HOW TO VALIDATE THAT THIS EXAMPLE IS COMPLIANT WITH THE RESPONSE MODEL": "NO BODY KNOWS",
                    "NOOOO BODY KNOOOOWS ": "BABY OOOH YEAAAAAHHH",
                    "AKTCHUALLLY": "SEE THE NEXT API TO KNOW HOW"
                }
            }
        }
    }
})
def create_cat(cat: CatCreate, db: Session = Depends(get_db)):
    return crud.create_cat(db=db, cat=cat)


cat_example_list = [
    Cat(
        id=2,
        birth_date="2021-05-15",
        paws_quantity=4,
        name="Mittens",
        gender="F",
        tails_quantity=1,
        rats_eaten=[
            Rat(
                id=1,
                birth_date="2022-03-01",
                courage=8,
                stupidity=3,
                is_eaten=True,
                cat_id=2
            ),
            Rat(
                id=2,
                birth_date="2022-03-01",
                courage=0,
                stupidity=10,
                is_eaten=True,
                cat_id=2
            )
        ]
    ),
    Cat(
        id=1,
        birth_date="2020-01-01",
        paws_quantity=4,
        name="Whiskers",
        gender="M",
        tails_quantity=1,
        rats_eaten=[]
    )
]


@app.get("/cats/", response_model=List[Cat], responses={
    200: {
        "description": "List of cats",
        "content": {
            "application/json": {
                "examples": {
                    "Example 1": {
                        "summary": "A list of cats -- a cat without a rat and a cat with two rats",
                        "value": [
                            Cat(
                                id=2,
                                birth_date="2021-05-15",
                                paws_quantity=4,
                                name="Mittens",
                                gender="F",
                                tails_quantity=1,
                                rats_eaten=[
                                    Rat(
                                        id=1,
                                        birth_date="2022-03-01",
                                        courage=8,
                                        stupidity=3,
                                        is_eaten=True,
                                        cat_id=2
                                    ),
                                    Rat(
                                        id=2,
                                        birth_date="2022-03-01",
                                        courage=0,
                                        stupidity=10,
                                        is_eaten=True,
                                        cat_id=2
                                    )
                                ]
                            ),
                            Cat(
                                id=1,
                                birth_date="2020-01-01",
                                paws_quantity=4,
                                name="Whiskers",gender="M",
                                tails_quantity=1,
                                rats_eaten=[]
                            )
                        ]
                    }
                }
            }
        }
    }})
def read_cats(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_cats(db=db, skip=skip, limit=limit)


@app.get("/cats/{cat_id}", response_model=Cat)
def read_cat(cat_id: int, db: Session = Depends(get_db)):
    db_cat = crud.get_cat(db=db, cat_id=cat_id)
    if db_cat is None:
        raise HTTPException(status_code=404, detail="Cat not found")
    return db_cat


@app.put("/cats/{cat_id}", response_model=Cat)
def update_cat(cat_id: int, cat: CatCreate, db: Session = Depends(get_db)):
    db_cat = crud.update_cat(db=db, cat_id=cat_id, cat=cat)
    if db_cat is None:
        raise HTTPException(status_code=404, detail="Cat not found")
    return db_cat


@app.delete("/cats/{cat_id}", response_model=Cat)
def delete_cat(cat_id: int, db: Session = Depends(get_db)):
    db_cat = crud.delete_cat(db=db, cat_id=cat_id)
    if db_cat is None:
        raise HTTPException(status_code=404, detail="Cat not found")
    return db_cat


# Rat endpoints
@app.post("/rats/", response_model=Rat)
def create_rat(rat: RatCreate, db: Session = Depends(get_db)):
    return crud.create_rat(db=db, rat=rat)


@app.get("/rats/", response_model=List[Rat])
def read_rats(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_rats(db=db, skip=skip, limit=limit)


@app.get("/rats/{rat_id}", response_model=Rat)
def read_rat(rat_id: int, db: Session = Depends(get_db)):
    db_rat = crud.get_rat(db=db, rat_id=rat_id)
    if db_rat is None:
        raise HTTPException(status_code=404, detail="Rat not found")
    return db_rat


@app.put("/rats/{rat_id}", response_model=Rat)
def update_rat(rat_id: int, rat: RatCreate, db: Session = Depends(get_db)):
    db_rat = crud.update_rat(db=db, rat_id=rat_id, rat=rat)
    if db_rat is None:
        raise HTTPException(status_code=404, detail="Rat not found")
    return db_rat


@app.delete("/rats/{rat_id}", response_model=Rat)
def delete_rat(rat_id: int, db: Session = Depends(get_db)):
    db_rat = crud.delete_rat(db=db, rat_id=rat_id)
    if db_rat is None:
        raise HTTPException(status_code=404, detail="Rat not found")
    return db_rat
