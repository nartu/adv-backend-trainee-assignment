import os
from settings import DB_CONNECT_CONFIG
from configparser import ConfigParser
import psycopg2

class Db:
    """psql connection"""

    def __init__(self, config=DB_CONNECT_CONFIG):
        super(Db, self).__init__()
        self.config = config

    def connect(self):
        # connect to db (without cursor)
        try:
            # read connection parameters
            params = self._parse_config()
            # connect to the PostgreSQL server
            conn = psycopg2.connect(**params)
            return conn
        except Exception as e:
            raise e

    def execute(self,sql='',force_answer=False,force_commit=False):
        # open, execute and close cursor
        # return dict: count of rows and list of tuples
        try:
            conn = self.connect()
            # print(conn)
            answer = {}
            with conn.cursor() as cur:
                sql = sql.strip()
                cur.execute(sql)
                answer['force_answer'] = force_answer
                answer['commit'] = True
                answer['rows'] = cur.rowcount
                if (force_answer or
                    sql.lower().find("select",0,6) != -1 or
                    sql.lower().find("show",0,4) != -1):
                    answer['psql_answer'] = \
                    [tuple(map(lambda x: x.strip() if type(x) is str else x,row))
                    for row in cur.fetchall()]
                    answer['commit'] = force_commit
                if answer['commit']:
                    if cur.rowcount > 0:
                        conn.commit()
                        # print('commit!')
                return answer
        except psycopg2.OperationalError as e:
            print("DB connection error: " + e.__class__.__name__)
            raise e
        except Exception as e:
            print("DB inner error: " + e.__class__.__name__)
            raise e

    def execute_one(self,sql=''):
        # open, execute for fetch only one row (ex. select * from table where id={}) and close cursor
        # return tuple
        try:
            conn = self.connect()
            # print(conn)
            with conn.cursor() as cur:
                cur.execute(sql)
                cur_result = cur.fetchone()
        except psycopg2.OperationalError as e:
            print("DB connection error: " + e.__class__.__name__)
            raise e
        except Exception as e:
            print("DB inner error: " + e.__class__.__name__)
            raise e

        if cur_result:
            return tuple(map(lambda x: x.strip() if type(x) is str else x,cur_result))
        return None

    def close(self):
        try:
            conn = self.connect()
            conn.close()
        except psycopg2.OperationalError as e:
            # come back to previous transaction
            print(e.__class__.__name__)
        except Exception as e:
            conn.rollback()
            raise e

    def _parse_config(self, section='postgresql'):
        # absolute path to connection config file
        filename = os.path.join(os.path.dirname(os.path.abspath(__file__)), self.config)
        # create a parser
        parser = ConfigParser()
        # read config file
        parser.read(filename)
        # get section, default to postgresql
        db = {}
        if parser.has_section(section):
            params = parser.items(section)
            for param in params:
                db[param[0]] = param[1]
        else:
            raise Exception('Section {0} not found in the {1} file'.format(section, filename))
        return db


def main():
     pass

if __name__ == '__main__':
    main()
