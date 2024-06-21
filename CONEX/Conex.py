import mysql.connector
import traceback

def conexion():
    try:
        myconn = mysql.connector.connect(host='localhost',
                        user='root',
                        passwd='',
                        database = 'masterbikes')
    except Exception as ex:
        print("Ocurrio un error", ex)

    return myconn
