from pydantic import BaseModel, ValidationError, validator, HttpUrl
from typing import Optional, List, Dict
from utils import db_create_ad

error = {}

class Image(BaseModel):
    url: HttpUrl
    # name: str

class NewAd(BaseModel):
    name: str
    description: str
    price: float
    images: Optional[List[Image]] = None

    @validator('name')
    def name_le200_and_title(cls, v, field):
        if len(v)>=200:
            # error.update({field.name: 'Must be less than 200 sympols'})
            raise ValueError(f'{field.name} must be less than 200 sympols')
        return v.title()

    @validator('description')
    def description_le1000_and_title(cls, v, field):
        if len(v)>=1000:
            # error.update({field.name: 'must be less than 1000 sympols'})
            raise ValueError(f'{field.name} must be less than 1000 sympols')
        return v

    @validator('images')
    def images_array_gt3(cls, v, field):
        if len(v)>3:
            raise ValueError(f'must be maximum 3 images')
        return v



def main():
    i1 = Image(url='https://cdn.britannica.com/s:690x388,c:crop/98/94698-050-F64C03A6/African-savanna-elephant.jpg')
    i2 = Image(url='https://cdn.britannica.com/s:690x388,c:crop/71/271-004-FC5E5FFB/Asian-elephant.jpg')
    i3 = Image(url='https://cdn.britannica.com/s:690x388,c:crop/02/152302-050-1A984FCB/African-savanna-elephant.jpg')
    p = NewAd(name='wqlw',description='test description',price=1,images=[i1,i2,i3])
    p2 = NewAd(name='Night',description='test description',price=1)

    # print(p.images[0].url)
    # print(p.__fields_set__)
    print(db_create_ad(p))

if __name__ == '__main__':
    main()


# try:
#     p = NewAd(name='wqlw',description='test description',price=1)
#     print(p.dict())
# except ValidationError:
#     e.update({'any': 'something wrong'})
# print(error)
