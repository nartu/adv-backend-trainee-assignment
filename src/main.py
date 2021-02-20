import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
# parentdir = os.path.dirname(currentdir)
sys.path.insert(0,currentdir)

from typing import Optional, List
from fastapi import FastAPI, Query, Path, HTTPException
from pydantic import BaseModel, ValidationError
from pmask import NewAd, GetOneAd
from utils import db_create_ad, db_get_ad_by_id
from pydantic.error_wrappers import ValidationError

# class NewAd(BaseModel):
#     name: str
#     description: str
#     price: float

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Ads API test app"}

# put new ad into bd
@app.post("/ads/create/")
async def create_ad(new:NewAd):
    id = db_create_ad(new)
    return {'id': id}

# detail of ad
# for post and get methods
def detail_of_ad_or_404(ad:GetOneAd):
    db_response = db_get_ad_by_id(ad)
    if db_response:
        return db_response
    else:
        raise HTTPException(status_code=404, detail="Not found")

@app.post("/ads/detail/{id}")
async def detail_of_ad_post(ad:GetOneAd):
    detail_of_ad_or_404(ad)

@app.get("/ads/detail/{id}")
async def detail_of_ad_get(id:str, fields:Optional[str] = None):
    if fields:
        fields = fields.split(',')
    else:
        fields = []
    try:
        ad = GetOneAd(id=id,fields=fields)
    except ValidationError as e:
        error = {'error': 'Validation Error',
                'loc': e.errors()[0]['loc'][0],
                'msg': e.errors()[0]['msg']}
        raise HTTPException(status_code=422, detail=error)

    return detail_of_ad_or_404(ad)
