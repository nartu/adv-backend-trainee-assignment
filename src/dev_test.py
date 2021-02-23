from utils import db_create_ad, db_get_ad_by_id, db_get_ads_list
from pmask import NewAd, Image, GetOneAd, GetListAds
import uuid
from pydantic.error_wrappers import ValidationError

def main():
    l = GetListAds(page=15, order={'price': 'desc', 'created_at': 'desc'})
    # print(l)
    # print(db_get_ads_list(l))
    # print(db_get_ads_list(l,'http://127.0.0.1:8000/'), sep='\n')

    # id_uuid = uuid.UUID('{bb432975-4e1b-4db5-86c9-0d37e04630e7}')
    #
    # a = GetOneAd(id='3fa85f64-5717-4562-b3fc-2c963f66afa6') # not exitst
    # b = GetOneAd(id='bb432975-4e1b-4db5-86c9-0d37e04630e7',fields=["photo", "description"])
    # c = GetOneAd(id='3d379544-3f50-45bb-be73-c34fafb8a1bb')
    #
    # print(db_get_ad_by_id(a))
    # print(db_get_ad_by_id(b))
    # print(db_get_ad_by_id(c))
    # try:
    #     print(GetOneAd(id='bb432975-4e1b-4db5-86c9-0d37e04630e700'))
    # except ValidationError as e:
    #     print(e.errors())
    #     print(dir(e))

    # print(a)

    i1 = Image(url='https://cdn.britannica.com/s:690x388,c:crop/98/94698-050-F64C03A6/African-savanna-elephant.jpg')
    i2 = Image(url='https://cdn.britannica.com/s:690x388,c:crop/71/271-004-FC5E5FFB/Asian-elephant.jpg')
    i3 = Image(url='https://cdn.britannica.com/s:690x388,c:crop/02/152302-050-1A984FCB/African-savanna-elephant.jpg')
    p = NewAd(name='Write 444',description='Mau description 333',price=23.11,images=[i1])
    p2 = NewAd(name='Night',description='test description',price=1)

    # print(p.images[0].url)
    # print(p.__fields_set__)
    print(db_create_ad(p))

    # print(uuid.UUID('{00010203-0405-0607-0809-0a0b0c0d0e0f}'))

if __name__ == '__main__':
    main()

# 0d3783e7-eef1-4d39-b3af-679125be9d20
# try:
#     p = NewAd(name='wqlw',description='test description',price=1)
#     print(p.dict())
# except ValidationError:
#     e.update({'any': 'something wrong'})
# print(error)

# Error ex.
# {
#   "detail": [
#     {
#       "loc": [
#         "body",
#         "price"
#       ],
#       "msg": "value is not a valid float",
#       "type": "type_error.float"
#     },
#     {
#       "loc": [
#         "body",
#         "images"
#       ],
#       "msg": "must be maximum 3 images",
#       "type": "value_error"
#     }
#   ]
# }
# error = []
# error += [{
#       "loc": [
#         "body",
#         "fields"
#       ],
#       "msg": f"wrong fields, possible values of fields: {available_fields_str}",
#       "type": "value_error"
#     }]
