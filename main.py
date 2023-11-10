from enum import Enum
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()


class DogType(str, Enum):
    terrier = "terrier"
    bulldog = "bulldog"
    dalmatian = "dalmatian"


class Dog(BaseModel):
    name: str
    pk: int
    kind: DogType


class Timestamp(BaseModel):
    id: int
    timestamp: int


dogs_db = {
    0: Dog(name='Bob', pk=0, kind='terrier'),
    1: Dog(name='Marli', pk=1, kind="bulldog"),
    2: Dog(name='Snoopy', pk=2, kind='dalmatian'),
    3: Dog(name='Rex', pk=3, kind='dalmatian'),
    4: Dog(name='Pongo', pk=4, kind='dalmatian'),
    5: Dog(name='Tillman', pk=5, kind='bulldog'),
    6: Dog(name='Uga', pk=6, kind='bulldog')
}

post_db = [
    Timestamp(id=0, timestamp=12),
    Timestamp(id=1, timestamp=10)
]


@app.get('/')
def root():
    return {"message": "Welcome to Veterinary Clinic Service"}


@app.post("/post", response_model=Timestamp)
def get_post():
    last_tstmp = post_db[-1]
    new_tstmp = Timestamp(id=last_tstmp.id+1, timestamp=last_tstmp.timestamp+1)
    post_db.append(new_tstmp)
    return new_tstmp


@app.post("/dog", response_model=Dog)
def create_dog(dog: Dog):
    dog.pk = len(dogs_db)  # changing pk for a unique sequential value
    dogs_db[len(dogs_db)] = dog
    return dog


@app.get("/dog", response_model=List[Dog])
def get_dogs(kind: DogType = None):
    if kind is None:
        return list(dogs_db.values())
    return [dog for dog in dogs_db.values() if dog.kind == kind]


@app.get("/dog/{pk}", response_model=Dog)
def get_dog_by_pk(pk: int):
    if pk not in dogs_db.keys():
        raise HTTPException(status_code=404, detail="Dog not found")

    else:
        return dogs_db[pk]


@app.patch("/dog/{pk}", response_model=Dog)
def update_dog(pk: int, updated_dog: Dog):
    if pk not in dogs_db.keys():
        raise HTTPException(status_code=404, detail="Dog not found")

    else:
        updated_dog = updated_dog.model_dump(exclude_unset=True)
        dogs_db[pk] = dogs_db[pk].model_copy(update=updated_dog)
        dogs_db[pk].pk = pk # to ensure primary key correctness

        return dogs_db[pk]
