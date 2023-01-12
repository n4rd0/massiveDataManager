import pymysql

def establecerConexion():
    #conexion a la bbdd 
    db = pymysql.connect(host = "localhost", 
                         user = "root", 
                         passwd = "7821", 
                         database = "tfg")
    return db
