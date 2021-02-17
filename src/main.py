import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
# parentdir = os.path.dirname(currentdir)
sys.path.insert(0,currentdir)

from typing import Optional
from fastapi import FastAPI, Query, Path
from pydantic import BaseModel
from pmask import NewAd, error
from utils import db_create_ad


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
