from typing import List, Dict
from db import Db
from pmask import NewAd, GetOneAd, GetListAds
from settings import ITEM_PER_PAGE

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

def db_get_ads_list(ads:GetListAds) -> Dict:
    ''' ads/list?page=1 , all ads by paginator,
        ads:
            page: int,
            order: Dict={'price': 'asc', 'created_at': 'asc'}
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
    db_res = db.execute(sql)
    db.close()

    return db_res['psql_answer']

def main():
    # print(db_get_ads_list(14), sep='\n')
    pass

if __name__ == '__main__':
    main()
