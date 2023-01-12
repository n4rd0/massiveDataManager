from Conector import establecerConexion

#Con esta funcion podemos agregar los estadios que queramos modularmente a la BBDD

def generarEstadio(NombreEstadio, Ubicacion, Secciones, Grupos, Filas, Asientos):

    #Creamor el cursor con el que comunicaremos con la bbdd
    db = establecerConexion()
    cursor = db.cursor()

    #ejecutamos la secuencia sql para sacar los ids y encontrar el mayor
    cursor.execute("SELECT idEstadio FROM tfg.estadio")
    idEstadios = cursor.fetchall()
    maxId = -1

    for x in idEstadios:
        if int(x[0]) > maxId: maxId = int(x[0])

    maxId += 1
    Capacidad = Secciones*Grupos*Filas*Asientos

    #Insertamos el estadio en la bbdd
    sql = """INSERT INTO `estadio` (idEstadio, NombreEstadio, 
    Capacidad, Ubicacion, Secciones, Grupos, Filas, Asientos) values(%s, %s, %s, %s, %s, %s, %s, %s)"""
    cursor.execute(sql, (maxId, NombreEstadio, Capacidad, Ubicacion, Secciones, Grupos, Filas, Asientos))
    db.commit()

