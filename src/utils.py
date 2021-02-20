from typing import List, Dict
from db import Db
from pmask import NewAd, GetOneAd

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
    inner join ads_photo as ph
    	on m.id = ph.main_id
    where m.id='{id}'
    {group_by_or_limit};
    '''

    db = Db()
    db.connect()
    bd_res = db.execute_one(sql)
    db.close()
    return bd_res
    result = {
        'name': bd_res[0],
        'price': float(bd_res[1]),
        'photo': bd_res[2],
    }

    if(description):
        result.update({'description': bd_res[3]})

    return result

def main():
    pass

if __name__ == '__main__':
    main()
