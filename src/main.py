import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
# parentdir = os.path.dirname(currentdir)
sys.path.insert(0,currentdir)

from typing import Optional, List
from fastapi import FastAPI, Query, Path, HTTPException
from pydantic import BaseModel, ValidationError
from pmask import NewAd, error
from utils import db_create_ad, db_get_ad_by_id

# class NewAd(BaseModel):
#     name: str
#     description: str
#     price: float

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Ads API test app"}

@app.post("/ads/create/")
async def create_ad(new: NewAd):
    id = db_create_ad(new)
    return {'id': id}

@app.post("/ads/detail/{id}")
async def detail_of_ad(fields: Optional[List[str]] = []):
    id = 'bb432975-4e1b-4db5-86c9-0d37e04630e7'
    error = []
    available_fields = ["photo","description"]
    available_fields_str = " ".join(available_fields)
    if len([item for item in fields if item not in available_fields])>0:
        error += [{
              "loc": [
                "body",
                "fields"
              ],
              "msg": f"wrong fields, possible values of fields: {available_fields_str}",
              "type": "value_error"
            }]
    if len(error)>0:
        raise HTTPException(status_code=422, detail=error)
    return db_get_ad_by_id(id,fields)
