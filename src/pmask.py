from pydantic import BaseModel, ValidationError, validator, HttpUrl, Field
from typing import Optional, List, Dict
from uuid import UUID

# error = {}
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

class GetOneAd(BaseModel):
    """Get ad from DB by id"""
    id: UUID
    addition_fields: Optional[List[str]] = Field([],alias='fields')

    @validator('addition_fields')
    def fields_available(cls, v, field):
        available_fields = ["photo","description"]
        available_fields_str = ", ".join(available_fields)
        if len([item for item in v if item not in available_fields])>0:
            raise ValueError(f"wrong fields, possible values of fields: {available_fields_str}")
        return v
