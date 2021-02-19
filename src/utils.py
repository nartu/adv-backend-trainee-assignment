from typing import List, Dict
from db import Db

def db_create_ad(post_data) -> str:
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

def db_get_ad_by_id(id:str = 'bb432975-4e1b-4db5-86c9-0d37e04630e7',fields:List=[]) -> Dict:
    ''' id: uuid, table ads_main + photo from ads_photo '''

    result = {}

    # if field off (empty list), sql query additions
    # description
    description = ''
    # photo
    photo, group_by_or_limit = 'ph.photo_url','limit 1'

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

    result = {
        'name': bd_res[0],
        'price': float(bd_res[1]),
        'photo': bd_res[2],
    }

    if(description):
        result.update({'description': bd_res[3]})

    return result

def main():
    # td1 = {'name': 'Wqlw', 'description': 'Test Description', 'price': 1.0, 'images': [{'url': HttpUrl('https://cdn.britannica.com/s:690x388,c:crop/98/94698-050-F64C03A6/African-savanna-elephant.jpg', scheme='https', host='cdn.britannica.com', tld='com', host_type='domain', path='/s:690x388,c:crop/98/94698-050-F64C03A6/African-savanna-elephant.jpg')}, {'url': HttpUrl('https://cdn.britannica.com/s:690x388,c:crop/71/271-004-FC5E5FFB/Asian-elephant.jpg', scheme='https', host='cdn.britannica.com', tld='com', host_type='domain', path='/s:690x388,c:crop/71/271-004-FC5E5FFB/Asian-elephant.jpg')}, {'url': HttpUrl('https://cdn.britannica.com/s:690x388,c:crop/02/152302-050-1A984FCB/African-savanna-elephant.jpg', scheme='https', host='cdn.britannica.com', tld='com', host_type='domain', path='/s:690x388,c:crop/02/152302-050-1A984FCB/African-savanna-elephant.jpg')}]}
    # p = db_create_ad()
    # print(p)

    # id ex bd264c47-525f-488a-982e-638fa074c441 , bb432975-4e1b-4db5-86c9-0d37e04630e7
    s = db_get_ad_by_id('bb432975-4e1b-4db5-86c9-0d37e04630e7',fields=['description'])
    # s = db_get_ad_by_id('bb432975-4e1b-4db5-86c9-0d37e04630e7')
    print(s.items())

if __name__ == '__main__':
    main()
