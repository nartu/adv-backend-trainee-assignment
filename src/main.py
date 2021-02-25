import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
# parentdir = os.path.dirname(currentdir)
sys.path.insert(0,currentdir)

from typing import Optional, List
from fastapi import FastAPI, Query, Path, HTTPException, Request, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ValidationError
from pmask import NewAd, GetOneAd, GetListAds
from utils import db_create_ad, db_get_ad_by_id, db_get_ads_list
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
@app.post("/ads/create", status_code=status.HTTP_201_CREATED,
    responses={
        201: {
            "description": "Item have created in DB",
            "content": {
                "application/json": {
                    "example": {"id": "id_uuid", "status": "Ok"}
                }
            },
        },
        503: {
            "description": "Validation is ok, but there's some inner error. Try later.",
            "content": {
                "application/json": {
                    "example": {"status": "fail", "detail": "description"}
                }
            },
        },
        # 422: {"model": NewAd, "description": "Validation error"}
    })
async def create_ad(new:NewAd):
    res = db_create_ad(new)
    if res["status"] == "fail":
        return JSONResponse(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, content=res)
    return res

# detail of ad
# for post and get methods
def detail_of_ad_or_404(ad:GetOneAd):
    db_response = db_get_ad_by_id(ad)
    if db_response:
        return db_response
    else:
        raise HTTPException(status_code=404, detail="Not found ad with this ID")

@app.post("/ads/detail")
async def detail_of_ad_post(ad:GetOneAd):
    return detail_of_ad_or_404(ad)

@app.get("/ads/detail/{id}")
async def detail_of_ad_get(id:str, fields:Optional[str] = None):
    if fields:
        fields = fields.split(',')
    else:
        fields = []

    try:
        ad = GetOneAd(id=id,fields=fields)
    except ValidationError as e:
        # error = {'error': 'Validation Error',
        #         'loc': e.errors()[0]['loc'][0],
        #         'msg': e.errors()[0]['msg']}
        raise HTTPException(status_code=422, detail=e.errors())

    return detail_of_ad_or_404(ad)

# list of ads
@app.post("/ads/list")
async def list_of_ads_post(request: Request, ads:GetListAds):
    res = db_get_ads_list(ads)
    if res.get("error") == "404":
        raise HTTPException(status_code=404, detail="Not found")
    elif res.get("error") == "204":
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)
    return res

@app.get("/ads/list/{page}")
async def list_of_ads_get(request: Request, page:int=1):
    try:
        ads = GetListAds(page=page)
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=e.errors())

    res = db_get_ads_list(ads, str(request.base_url))
    if res.get("error" == "404"):
        raise HTTPException(status_code=404, detail="Not found")
    elif res.get("error") == "204":
        return JSONResponse(status_code=200, \
            content={"detail": "No ads yet. Try /ads/create via POST"})
    return res
