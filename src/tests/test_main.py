import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)
# print(sys.path)

from main import app
from fastapi.testclient import TestClient
from fastapi.encoders import jsonable_encoder
import datetime
import pytest
from settings import ITEM_PER_PAGE

client = TestClient(app, base_url="http://127.0.0.1:8000")

# params
params_get = [
    # legal
    ({}, ['name', 'price', 'photo'],200),
    ({'fields':''}, ['name', 'price', 'photo'],200),
    ({'fields':'description'}, ['name', 'price', 'photo','description'],200),
    ({'fields':'photo'}, ['name', 'price', 'photo'],200),
    ({'fields':'photo,description'}, ['name', 'price', 'photo','description'],200),
    # ?fields=photo&fields=description for get
    ({'fields':['photo','description']}, ['name', 'price', 'photo','description'],200),
    # validation error
    ({'fields':'image'}, ['detail'],422),   # wrong value
    # ignore param, some feied (mb must be fix but not important)
    ({'field':'photo'}, ['name', 'price', 'photo'],200),
]

params_post = [
    # legal
    ({'fields':[]}, ['name', 'price', 'photo'],200),
    ({'fields':['description']}, ['name', 'price', 'photo','description'],200),
    ({'fields':['photo','description']}, ['name', 'price', 'photo','description'],200),
    # validation error
    ({'fields':['image']}, ['detail'],422),   # wrong value
    ({'fields':''}, ['detail'],422), # value must be array
    # ignore param, some feied (mb must be fix but not important)
    ({'field':['photo']}, ['name', 'price', 'photo'],200),
]

# CREATE
def test_ads_create_success():
    global id
    name_suffix = str(int(datetime.datetime.now().timestamp()))[-4::1]
    j1 = {
      "name": f"Test product {name_suffix}",
      "description": f"Description of product {name_suffix}",
      "price": 12
    }
    r = client.post("/ads/create", json=j1)
    assert r.json().get("status") == "ok"
    assert len(r.json().get("id")) == 36
    # id for next test
    id = r.json().get("id")

def test_ads_create_fail():
    j2 = {
        # name must be max 200 simbols
        "name": "a"*201,
        # name must be max 1000 simbols
        "description": "a"*1001,
        # price must be digit (float,int,'digit') -> float
        "price": "one ruble",
        # images must be array <=3 of obj.url with url scheme
        # can be without images (array of obj)
        "images": [
            {"url":"http://example.com/img1.jpg"},
            {"url":"http://example.com/img2.jpg"},
            {"url":"http://example.com/img3.jpg"}
        ]
    }
    r = client.post("/ads/create", json=j2)
    assert r.status_code == 422
    assert len(r.json().get("detail")) == 3

def test_ads_create_fail_images():
    # right params
    j3 = {
        "name": "It's ok name",
        "description": "It's ok description",
        "price": 21,
    }

    # wrong type of images: must be array
    j4 = {**j3, "images": "http://example.com/img.jpg"}
    r4 = client.post("/ads/create", json=j4)
    assert r4.status_code == 422
    assert len(r4.json().get("detail")) == 1
    assert r4.json().get("detail")[0]["loc"][1] == "images"

    # image must have url scheme
    j5 = {**j3, "images": ["img.jpg"]}
    r5 = client.post("/ads/create", json=j5)
    assert r5.status_code == 422
    assert len(r5.json().get("detail")) == 1
    assert r5.json().get("detail")[0]["loc"][1] == "images"

    # images must be array and <=3 obj {"url":"http://e.com"} with url scheme
    # "msg": "must be maximum 3 images"
    images = [
        {"url":"http://example.com/img1.jpg"},
        {"url":"http://example.com/img2.jpg"},
        {"url":"http://example.com/img3.jpg"},
        {"url":"http://example.com/img4.jpg"}
    ]
    j6 = {**j3, "images": images}
    r6 = client.post("/ads/create", json=j6)
    assert r6.status_code == 422
    assert len(r6.json().get("detail")) == 1
    assert r6.json().get("detail")[0]["loc"][1] == "images"
    assert r6.json().get("detail")[0]["msg"] == "must be maximum 3 images"

# GET ONE
@pytest.mark.parametrize(
    ('addition_params','response_body_keys_ar','response_status'),
    params_post
)
def test_ads_detail_post(addition_params, response_body_keys_ar, response_status):
    global id
    r = client.post("/ads/detail", json={"id":id,**addition_params})
    # print(r.json().keys())
    # print(r.url)
    assert r.status_code == response_status
    assert list(r.json().keys()) == response_body_keys_ar

@pytest.mark.parametrize(
    ('addition_params','response_body_keys_ar','response_status'),
    params_get
)
def test_ads_detail_get(addition_params, response_body_keys_ar, response_status):
    global id
    path = os.path.join("/ads/detail",id)
    r = client.get(path, params=addition_params)
    assert r.status_code == response_status
    assert list(r.json().keys()) == response_body_keys_ar

# GET LIST
def test_ads_list_post():
    # without params, page by default = 1
    r = client.post("/ads/list", json={})
    assert r.status_code == 200
    total_pages = r.json().get("total_pages")
    total_items = r.json().get("total_items")

    # paginator and order price asc (by default: {'price': 'asc', 'created_at': 'asc'})
    previous = 0
    for page in range(1,total_pages+1):
        j = {"page": page, "order":{'price': 'asc'}}
        r = client.post("/ads/list", json=j)
        items = len(r.json().get("data"))
        # items per page
        assert items == ITEM_PER_PAGE if page != total_pages \
                else total_items-(page-1)*ITEM_PER_PAGE
        # order asc, last previous must be max
        last_price = float(r.json().get("data")[items-1].get("price"))
        assert previous <= last_price
        previous = last_price
    # paginator and order price desc
    for page in range(1,total_pages+1):
        j = {"page": page, "order":{'price': 'desc', 'created_at': 'asc'}}
        r = client.post("/ads/list", json=j)
        assert r.status_code == 200
        # order desc, last previous must be min
        last_price = float(r.json().get("data")[items-1].get("price"))
        assert previous >= last_price
        previous = last_price

    # if page>total_pages must be detail_of_ad_or_404
        j = {"page": total_pages+1}
        r = client.post("/ads/list", json=j)
        assert r.status_code == 404

def main():
    test_ads_create_success()


if __name__ == '__main__':
    main()
