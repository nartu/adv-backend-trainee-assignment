from typing import List, Dict
from db import Db
from pmask import NewAd, GetOneAd, GetListAds
from settings import ITEM_PER_PAGE
import os
from urllib.parse import urljoin
import math

def db_create_ad(post_data:NewAd) -> str:
    p = post_data
    sql_return_last_id = ''
    if 'images' in p.__fields_set__ and len(p.images)>0:
        sql_insert_image_values = ''
        i = 1
        for image in p.images:
            sep = '' if i==len(p.images) else ','
            sql_insert_image_values += f'''
            ((SELECT * FROM last_main_id),
            '{image.url}')'''+sep+'\n'
            i += 1
        sql_return_last_id = f'''
            INSERT INTO ads_photo (main_id,photo_url)
            VALUES
            {sql_insert_image_values}
        	RETURNING main_id;
            '''
    else:
        sql_return_last_id = '''
        SELECT * FROM last_main_id;
        '''

    sql = f'''
        WITH last_main_id AS
        	(INSERT INTO ads_main (name, description, price)
        			VALUES ('{p.name}','{p.description}','{p.price}') RETURNING id)
        {sql_return_last_id}
    '''
    db = Db()
    db.connect()
    bd_res = db.execute(sql,force_answer=True,force_commit=True)
    db.close()
    res = sql
    return bd_res['psql_answer'][0][0]

def db_get_ad_by_id(ad:GetOneAd) -> Dict:
    ''' id: uuid, table ads_main + photo from ads_photo '''

    id = ad.id
    # id = 'bb432975-4e1b-4db5-86c9-0d37e04630e7'

    fields = ad.addition_fields

    result = {}

    # if fields off (empty list), sql query additions
    # description
    description = ''
    # photo
    photo = 'ph.photo_url'
    group_by_or_limit = 'limit 1'

    if('description' in fields):
        description = ', m.description'

    if('photo' in fields):
        photo = 'array_agg(ph.photo_url)'
        group_by_or_limit = 'group by m.id'

    sql = f'''
    select m.name, m.price, {photo} {description} from ads_main as m
    left join ads_photo as ph
    	on m.id = ph.main_id
    where m.id='{id}'
    {group_by_or_limit};
    '''

    db = Db()
    db.connect()
    db_res = db.execute_one(sql)
    db.close()

    if db_res:
        result = {
            'name': db_res[0],
            'price': float(db_res[1]),
            'photo': db_res[2],
        }
        if(description):
            result.update({'description': db_res[3]})
    else:
        result = None

    return result

def db_get_ads_list(ads:GetListAds, base_url:str='') -> Dict:
    ''' ads/list?page=1 , all ads by paginator,
        ads:
            page: int,
            order: Dict={'price': 'asc', 'created_at': 'asc'}
        base_url: for path to detail of ad, request.base_url
    '''
    page = ads.page
    order = ads.order

    if order and len(order)>0:
        order_by = 'order by '
        order_by_items = []
        for k,v in order.items():
    		# m.price asc,
            order_by_items += [f'm.{k} {v}']
        order_by += ", ".join(order_by_items)
    else:
        order_by = ''

    limit = ITEM_PER_PAGE
    offset = (page-1) * ITEM_PER_PAGE

    sql = f'''
    select m.id, m.name, m.price, (array_agg(ph.photo_url))[1]
    -- , m.description, (array_agg(ph.photo_url))
    from ads_main m
    left join (select photo_url, main_id from ads_photo) ph
    on m.id = ph.main_id
    group by m.id
	{order_by}
    offset {offset} limit {limit};
    '''

    # return sql

    db = Db()
    db.connect()

    # total count of items and pages
    # error 404 if page > total_pages (empty result from db)
    total_items = db.execute_one("select sum(1) from ads_main;")[0]
    total_pages = math.ceil(total_items/ITEM_PER_PAGE)
    if page > total_pages:
        db.close()
        error = {"error":"404"}
        return error

    result = {
        "total_items": total_items,
        "total_pages": total_pages,
        "current_page": page,
    }

    db_res = db.execute(sql)

    db.close()

    result.update({"data": []})
    if len(db_res)>0:
        for item in db_res['psql_answer']:
            # http://example.com/ads/detail/{id}
            id = item[0]
            url_path = os.path.join('/','ads/detail', id)
            url = urljoin(base_url, url_path)
            result["data"].append({
                "url": url,
                "name": item[1],
                "price": item[2],
                "photo": item[3],
            })

    return result


def main():
    # print(db_get_ads_list(14), sep='\n')
    pass

if __name__ == '__main__':
    main()
