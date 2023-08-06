import pymysql
import icepy.config as config
import traceback
import datetime
import sys
from icepy.config import ICE
import pandas as pd
import numpy as np

class DB():
    def __init__(self, host=ICE.MYSQL_HOST, port=ICE.MYSQL_PORT, user=ICE.MYSQL_USER, passoword=ICE.MYSQL_PASSWD,database=ICE.MYSQL_DBNAME,charset='utf8'):
        self.db =pymysql.connect(
            host = host,
            port =port,
            user=user,
            password=passoword,
            database = database,
            charset = charset
        )
        # Get a cursor
        self.cursor = self.db.cursor()


    def __enter__(self):
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cursor.close()
        self.db.close()

    def createTable_baseline(self):
    #Create table
        self.cursor.execute("DROP TABLE IF EXISTS building")
        sql = """CREATE TABLE baseline (
            ID INT AUTO_INCREMENT NOT NULL UNIQUE PRIMARY KEY,
            NAME  VARCHAR(45),
            PATH VARCHAR(255),
            PARENT  TINYINT"""

        self.cursor.execute(sql)

    def createTable_simulation_info(self):
    #Create table
        self.cursor.execute("DROP TABLE IF EXISTS model")
        sql = """CREATE TABLE model (
            ID INT AUTO_INCREMENT NOT NULL UNIQUE PRIMARY KEY,
            BID INT,
            NAME  VARCHAR(100),
            HEIGHT FLOAT ,
            CEILING_HT FLOAT,
            DATETIME DATETIME_INTERVAL_CODE,
            PATH VARCHAR(255),
            NOTE VARCHAR(100)
            PARENT  TINYINT"""

        self.cursor.execute(sql)

    def createTable_simu_results(self):
    #Create table
        self.cursor.execute("DROP TABLE IF EXISTS simulation")
        sql = """CREATE TABLE simulation (
            ID INT AUTO_INCREMENT NOT NULL UNIQUE PRIMARY KEY,
            SID INT,
            WWR_RATIO FLOAT ,
            TOTAL_TIME FLOAT,
            SIMU_TIME FLOAT,
            KWH FLOAT ,
            KWH_PER_M2 FLOAT ,
            PATH VARCHAR(255),
            PARENT  TINYINT"""

        self.cursor.execute(sql)

    # Insert the baseline model and return bid
    def insert_building(self, name, path, table_name = "`building`"):
        sql1 = "INSERT IGNORE INTO " + table_name + " (name, path) VALUES (%s, %s)"
        sql1 = "insert into " + table_name + " (id, name, path)\
                select null, %s, %s from DUAL\
                where not exists (select id from building where name = %s)"
        value1 = (name, path, name)
        self.cursor.execute(sql1, value1)

        try:
            self.cursor.execute(sql1, value1)
            self.db.commit()
            sqlq = "SELECT * FROM " + table_name + " WHERE `name` = %s"
            valq = (name,)
            self.cursor.execute(sqlq, valq)

            return self.cursor.fetchone()[0]

        except:
            # If error, rollback
            self.db.rollback()
            print("Exception in user code:")
            print('-' * 60)
            traceback.print_exc(file=sys.stdout)
            print('-' * 60)
            print('The building name already exists.')
            return False

    # Insert simulation inforation ,return sid
    def insert_model(self, bid, height, ceiling_ht, num_floor, path, name, note, table_name = "`model`"):
        now = datetime.datetime.now()
        formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')

        sql1 = "INSERT INTO " + table_name + " (bid,height, ceiling_ht, num_floor, path, name, datetime, note) " \
                                             "VALUES (%s,%s,%s,%s,%s,%s,%s, %s)"
        value1 = (bid, height, ceiling_ht, num_floor, path, name, formatted_date, note)
        try:
            self.cursor.execute(sql1, value1)
            self.db.commit()
            sid = self.cursor.lastrowid
            return sid
        except:
            self.db.rollback()
            return False

    # Insert simulation results
    def insert_simulation(self, sid, wwr_ratio, total_time, simu_time, kwh, kwh_per_m2, path,
                  table_name="`simu_results`"):  # fisrt non-defalut argument, then default argument


        sql2 = "INSERT INTO " + table_name + " (sid,wwr_ratio, total_time, simu_time, kwh, kwh_per_m2, path) \
                    VALUES (%s,%s, %s, %s, %s, %s, %s)"
        value = (sid, wwr_ratio, total_time, simu_time, kwh, kwh_per_m2, path)


        try:
            # 执行sql语句
            self.cursor.execute(sql2, value)
            # 提交到数据库执行
            self.db.commit()
        except:
            # 如果发生错误则回滚
            self.db.rollback()
            print("Exception in user code:")
            print('-' * 60)
            traceback.print_exc(file=sys.stdout)
            print('-' * 60)


    def insert_computational_df_html(self, base, building_ht, folder, floor_ht, num_floors,new_name, note, computational, dfs, html_dicts):

        bid = self.insert_building(base, folder + base + '.idm')

        #  bid, height, ceiling_ht, num_floor, path, name, note
        sid = self.insert_model(bid, building_ht, floor_ht, num_floors, folder, new_name, note)

        # sid, bid, wwr_ratio, total_time, simu_time, kwh, kwh_per_m2, path,
        for x in computational:
            wwr_ratio = x['wwr_ratio']
            kwh = 0
            kwh_per = 0
            path = folder+base+'.idm'

            for k in html_dicts:
                if k['wwr_ratio'] == wwr_ratio:
                    path = k['html']

            for y in dfs:
                if float(y.loc[y['facility'] == 'Grand total']['wwr_ratio']) == wwr_ratio:
                    a = y.loc[y['facility'] == 'Grand total']
                    kwh = float(a['kwh'])
                    kwh_per = float(a['kwh/m2'])

            print(sid, wwr_ratio, x['total_time'], x['simu_time'], kwh, kwh_per, path)
            self.insert_simulation(sid, wwr_ratio, x['total_time'], x['simu_time'], kwh, kwh_per, path)




    def query_building(self, name, table_name = "`building`"):
        sql = "select * from "+ table_name + " where `name` = %s"
        value = (name,)

        try:
            self.cursor.execute(sql, value)
            dict = {}
            a = self.cursor.fetchone()
            dict['bid'] = a[0]
            dict['name'] = a[1]
            dict['path'] = a[2]
            return dict
        except:
            # 如果发生错误则回滚
            self.db.rollback()
            print("Exception in user code:")
            print('-' * 60)
            traceback.print_exc(file=sys.stdout)
            print('-' * 60)

    def query_model(self, name, table_name = "`model`"):
        sql = "select * from "+ table_name + " where `name` = %s"
        value = (name,)

        try:
            self.cursor.execute(sql, value)
            dict = {}
            a = self.cursor.fetchone()
            dict['sid'] = a[0]
            dict['bid'] = a[1]
            dict['height'] = a[2]
            dict['ceiling_ht'] = a[3]
            dict['num_floor'] = a[4]
            dict['datetime'] = a[5]
            dict['path'] = a[6]
            dict['name'] = a[7]

            return dict
        except:
            # 如果发生错误则回滚
            self.db.rollback()
            print("Exception in user code:")
            print('-' * 60)
            traceback.print_exc(file=sys.stdout)
            print('-' * 60)

    def query_simulation(self, sid, table_name = "`simulation`"):
        sql = "select * from "+ table_name + " where `sid` = %s"
        value = (sid,)

        try:
            self.cursor.execute(sql, value)
            dict = {}
            a = self.cursor.fetchone()
            dict['id'] = a[0]
            dict['sid'] = a[1]
            dict['wwr_ratio'] = a[2]
            dict['total_time'] = a[3]
            dict['simu_time'] = a[4]
            dict['kwh'] = a[5]
            dict['kwh_per_m2'] = a[6]
            dict['path'] = a[7]

            return dict
        except:
            # 如果发生错误则回滚
            self.db.rollback()
            print("Exception in user code:")
            print('-' * 60)
            traceback.print_exc(file=sys.stdout)
            print('-' * 60)

  #  "`simu_results`"   "`simulation_info`"  "`baseline`"
    def sql2df(self, name_tab_str):
        # 获取表内数据
        sql_data = '''select * from %s; ''' % name_tab_str
        self.cursor.execute(sql_data)
        data = self.cursor.fetchall()
        # 获取列名
        cols = [i[0] for i in self.cursor.description]
        # sql内表转换pandas的DF
        df = pd.DataFrame(np.array(data), columns=cols)
        return df






# unit test
class TestDBHelper():
    def __init__(self):
        self.db = DB()

    # test insert_baseline
    def testInsertBaseline(self):
        return self.db.insert_building("ut1", 22.5, 'D:\\ide_mine\\changing\\ut1.idm')

    # test insert_simulation_info
    def testInsertSimulation_info(self):
        return self.db.insert_model(1,22.5, 3, 5, 'D:\\ide_mine\\changing\\ut1_5floor.idm', 'ut1_5floor')

    # test insert_simu_results
    def testInsertSimuResults(self):
        return self.db.insert_simulation(1,1, 0.45, 227.111, 225.111, 532992, 182.5, 'D:\\ide_mine\\changing\\ut1_5floor_0.45.idm')

    def testQueryBaseline(self):
        return self.db.query_building('ut1')

    def testQuerySimu_results(self):
        return self.db.query_simulation('1')

    def test_sql2df(self):
        print(self.db.sql2df("`simulation`"))


if __name__ == '__main__':
    test1 = TestDBHelper()
    # print(test1.testInsertBaseline())
    # test1.testInsertSimulation_info()
    # test1.testInsertSimuResults()
    print(test1.testQuerySimu_results())