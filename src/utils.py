from typing import List, Dict
from db import Db

def db_create_ad(post_data):
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


def main():
    # td1 = {'name': 'Wqlw', 'description': 'Test Description', 'price': 1.0, 'images': [{'url': HttpUrl('https://cdn.britannica.com/s:690x388,c:crop/98/94698-050-F64C03A6/African-savanna-elephant.jpg', scheme='https', host='cdn.britannica.com', tld='com', host_type='domain', path='/s:690x388,c:crop/98/94698-050-F64C03A6/African-savanna-elephant.jpg')}, {'url': HttpUrl('https://cdn.britannica.com/s:690x388,c:crop/71/271-004-FC5E5FFB/Asian-elephant.jpg', scheme='https', host='cdn.britannica.com', tld='com', host_type='domain', path='/s:690x388,c:crop/71/271-004-FC5E5FFB/Asian-elephant.jpg')}, {'url': HttpUrl('https://cdn.britannica.com/s:690x388,c:crop/02/152302-050-1A984FCB/African-savanna-elephant.jpg', scheme='https', host='cdn.britannica.com', tld='com', host_type='domain', path='/s:690x388,c:crop/02/152302-050-1A984FCB/African-savanna-elephant.jpg')}]}
    # p = db_create_ad()
    # print(p)
    pass

if __name__ == '__main__':
    main()
