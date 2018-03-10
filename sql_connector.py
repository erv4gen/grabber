import pyodbc
import pandas as pd
import variables
import doc_transform
import time
import datetime

def push_to_server(site, url, meta, title, body):
    try:
        # -----------LOGIN INFORMATION-----------
        server = '-'
        database = '-'
        username = '-'
        password = '-'
        driver = '{ODBC Driver 13 for SQL Server}'

        # ----------------------------------------
        cnxn = pyodbc.connect('DRIVER=' + driver + ';PORT=1433;SERVER=' + server + ';PORT=1443;DATABASE='
                              + database + ';UID=' + username + ';PWD=' + password)
        cursor = cnxn.cursor()
        print("Connected successfully")
        # --------Values to pass-----------------
        site_title = "[{}]".format(str(site))
        qurl = ""'{}'"".format(str(url))
        qmeta = ""'{}'"".format(str(meta))
        qtitle = ""'{}'"".format(str(title))
        qbody = ""'{}'"".format(str(body))
        bu = ""'{}'"".format(str(variables.bu))
        div = ""'{}'"".format(str(variables.div))
        ent = ""'{}'"".format(str(variables.ent))
        # ----------------------------------------


        sql1 = """IF NOT EXISTS
         ( SELECT [name] FROM sys.tables WHERE [name] = '{}' ) 
         CREATE TABLE {} (
         ID int IDENTITY(1,1) PRIMARY KEY
         , URL varchar(MAX)
         , META varchar(MAX)
         , TITLE varchar(MAX)
         , BODY varchar(MAX)
         ,BU varchar(MAX)
         , DIV varchar(MAX)
         , ENT varchar(MAX))
        """.format(site, site_title)

        cursor.execute(sql1)
        cnxn.commit()


        sql2 = """INSERT INTO [dbo].{} ([URL],[META],[TITLE],[BODY],[BU],[DIV],[ENT]) VALUES(?,?,?,?,?,?,?)""".format(site_title)

        cursor.execute(sql2,
                       qurl,
                       qmeta,
                       qtitle,
                       qbody,
                       bu,
                       div,
                       ent)
        cnxn.commit()
        print('Pushed successfully to table: '+str(site))
    except pyodbc.Error as err:
        print(format(err))
        print("--")


    except Exception as e:
        print(e)

    finally:
        cursor.close()
        del cursor
        cnxn.close()


def get_work_list(table):
    try:
        # -----------LOGIN INFORMATION-----------
        server = '-'
        database = '-'
        username = '-'
        password = '-'
        driver = '{ODBC Driver 13 for SQL Server}'

        # ----------------------------------------
        cnxn = pyodbc.connect('DRIVER=' + driver + ';PORT=1433;SERVER=' + server + ';PORT=1443;DATABASE='
                              + database + ';UID=' + username + ';PWD=' + password)
        #cursor = cnxn.cursor()
        print("Connected successfully")



        sql1 = """SELECT  [website]
      ,[BU ]
      ,[Division ]
      ,[Entity]
        FROM [dbo].[{}]
            """.format(table)

        data_frame = pd.read_sql(sql1, cnxn)
        print('Got List of sites...starting work')

        return data_frame
    except pyodbc.Error as err:
        print(format(err))
        print("--")

    except:
        pass

    finally:
        #cursor.close()
        #del cursor
        cnxn.close()


def add_to_log(row):
    try:
        # -----------LOGIN INFORMATION-----------

        server = '-'
        database = '-'
        username = '-'
        password = '-'
        driver = '{ODBC Driver 13 for SQL Server}'

        # ----------------------------------------
        cnxn = pyodbc.connect('DRIVER=' + driver + ';PORT=1433;SERVER=' + server + ';PORT=1443;DATABASE='
                              + database + ';UID=' + username + ';PWD=' + password)

        new_row = row
        new_row['date'] = datetime.date.today()
        new_row['status'] = 'done'
        cursor = cnxn.cursor()


        # --------Values to pass-----------------
        table_name = "[{}]".format("log_file")
        site_title = ""'{}'"".format(str(new_row['website']))
        date_ = ""'{}'"".format(str(new_row['date']))
        status = ""'{}'"".format(str(new_row['status']))

        # ----------------------------------------

        sql1 = """IF NOT EXISTS
                 ( SELECT [name] FROM sys.tables WHERE [name] = '{}' ) 
                 CREATE TABLE {} (
                 ID int IDENTITY(1,1) PRIMARY KEY
                 , Date Datetime NULL
                 , Site varchar(MAX)
                 , Stats varchar(MAX))
                """.format('log_file', table_name)

        cursor.execute(sql1)
        cnxn.commit()

        sql2 = """INSERT INTO [dbo].{} ([Date],[Site],[Stats]) VALUES(?,?,?)""".format(
            table_name)

        cursor.execute(sql2,
                       date_,
                       site_title,
                       status)
        cnxn.commit()
        print('Pushed successfully')

    except pyodbc.Error as err:
        print(format(err))
        print("--")


    except Exception as e:
        print(e)

    finally:
        cursor.close()
        del cursor
        cnxn.close()


