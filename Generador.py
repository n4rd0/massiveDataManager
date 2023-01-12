import random 
from  Asistente import Asistente
from Conector import establecerConexion

"""
Clase encargada de generar los datos de asistentes que compran y venden entradas para los estadios. 

"""
l = open('metadata/Names.txt','r')
listaNombres = l.readlines()
l = open('metadata/Surnames.txt','r')
listaApellidos = l.readlines()
l = open('metadata/Alphabet.txt', 'r')
alphabet = l.readlines()
l.close()

#Previo a la ejecucion actualoizamos en el diccionario dicIdPlazasDisponibles que plazas del estadio estan vacias, esto se hace con el total menos las ocupadas
def actualizarPlazas():
    db = establecerConexion()
    cursor = db.cursor()
    
    global nEstadios
    nEstadios = cursor.execute("SELECT * FROM tfg.estadio")
    
    global idEstadios
    cursor.execute("SELECT idEstadio FROM tfg.estadio")  
    idEstadios = cursor.fetchall()

    global dicIdPlazasDisponibles
    global dicIdPlazasOcupadas 
    global estadiosDisponibles
    
    estadiosDisponibles = []
    dicIdPlazasDisponibles = {}
    dicIdPlazasOcupadas = {}

    for id in idEstadios:
        estadiosDisponibles.append(id[0])
        cursor.execute("SELECT Secciones, Grupos, Filas, Asientos FROM tfg.estadio WHERE IdEstadio = %s",id[0])
        dimensionesEstadio = cursor.fetchall()
        plazasDisponibles = []
        pOcupadas = []

        for i in range(1,dimensionesEstadio[0][0]+1):
            seccion = "0"+str(i)
            seccion = seccion[-2:]
            for j in range(1,dimensionesEstadio[0][1]+1):
                grupo = "0"+str(j)
                grupo = grupo[-2:]
                for k in range(1,dimensionesEstadio[0][2]+1):
                    fila = "0"+str(k)
                    fila = fila[-2:]
                    for l in range(1,dimensionesEstadio[0][3]+1):
                        asiento = "0"+str(l)
                        asiento = asiento[-2:]
                        plazasDisponibles.append(seccion+grupo+fila+asiento)

        cursor.execute("SELECT PlazaEstadio FROM tfg.asistente WHERE IdEstadio = %s ",id[0])
        plazasOcupadas = cursor.fetchall()

            
        for plazaOcupada in plazasOcupadas:
            pOcupadas.append(plazaOcupada[0])
            plazasDisponibles.remove(plazaOcupada[0])

        dicIdPlazasDisponibles[id[0]] = plazasDisponibles
        dicIdPlazasOcupadas[id[0]] = pOcupadas

#Eliminar asistentes del estadio por nombre
def eliminarAsistentes(numeroEliminaciones):


        asistentesAEliminar = []
        #Sacamos la id del estadio asociada al nombre

        for _ in range(numeroEliminaciones):

            if len(estadiosDisponibles)> 0:
                idEstadio = estadiosDisponibles[random.randint(0, len(estadiosDisponibles)-1)]
            else:
                continue

            if len(dicIdPlazasOcupadas[idEstadio])>0:

                plazaAsistenteEliminar = dicIdPlazasOcupadas[idEstadio][random.randint(0, len(dicIdPlazasOcupadas[idEstadio])-1)]
                dicIdPlazasDisponibles[idEstadio].append(plazaAsistenteEliminar)
                dicIdPlazasOcupadas[idEstadio].remove(plazaAsistenteEliminar)
                asistentesAEliminar.append(plazaAsistenteEliminar)
            
            else:
                estadiosDisponibles.remove(idEstadio)
        
        eliminarAsistentesBaseDatos(asistentesAEliminar)

#Genera el numero indicado de asistentes
def generarAsistentes(numeroGeneraciones):

    #Accedemos a distitnas bases de datos de nombres y apellidos para posterior
    #mente generar aleatoriamente los datos
    listaAsistentesGenerada = []

    for _ in range(numeroGeneraciones):


        #Generamos al azar en cual de todos los estadios nuestro asistente 
        #ficticio estara alojandose
        if len(estadiosDisponibles)> 0:
            idEstadio = estadiosDisponibles[random.randint(0, len(estadiosDisponibles)-1)]
        else:
            continue
        #print(len(dicIdPlazasDisponibles[idEstadio]), idEstadio)
        if len(dicIdPlazasDisponibles[idEstadio])>0:

            if idEstadio not in estadiosDisponibles:
                estadiosDisponibles.append(idEstadio)
            #Cogemos un nombre y apellido al azar de las listas proporcionadas
            nombre = listaNombres[random.randint(0,len(listaNombres)-1)]
            apellido = listaApellidos[random.randint(0,len(listaApellidos)-1)]
            
            #La edad tambien se genera al azar entre 6 y 99
            edad = random.randint(6,99)
            
            #Para el DNI cogemos un numero al azar y calculamos el modulo para 
            #Asignarle una letra
            DNI = random.randint(0,99999999)
            DNI = str(DNI) + alphabet[DNI%len(alphabet)]
            
            #La plaza depende del estadio elegido obteniendola igual de forma aleatoria

            plazaEstadio = dicIdPlazasDisponibles[idEstadio][random.randint(0,len(dicIdPlazasDisponibles[idEstadio])-1)]
            dicIdPlazasDisponibles[idEstadio].remove(plazaEstadio)
            dicIdPlazasOcupadas[idEstadio].append(plazaEstadio)

            #Obtenemos todos los estadios almacenados en la bbdd
            
            asist = Asistente(idEstadio, nombre.strip(), apellido.strip(), edad, DNI.strip(), plazaEstadio)
            listaAsistentesGenerada.append(asist)

    #print(listaAsistentesGenerada[0])
    insertarAsistenteBaseDatos(listaAsistentesGenerada)
        

#Actualzia en la bbdd el porcentaje de llenado del estadio
def modificarPorcentajeLleno(idEstadio):

    db = establecerConexion()
    cursor = db.cursor()

    #Sacamos el total de asientos ocupados en el estadio
    asientosOcupados = cursor.execute("SELECT * FROM tfg.asistente WHERE idEstadio = %s", idEstadio)
    cursor.execute("SELECT Secciones, Grupos, Filas, Asientos FROM tfg.estadio WHERE idEstadio = %s", idEstadio)

    #Sacamos la capacidad del estadio
    datos = cursor.fetchall()
    capacidad = datos[0][0]*datos[0][1]*datos[0][2]*datos[0][3]

    #Calculamos el porcentaje
    porcentajeLLeno = round(asientosOcupados*100/capacidad,4)

    #Ejecutamos la actualizacion del porcentaje en la bbdd
    cursor.execute("UPDATE tfg.estadio SET PorcentajeLLeno = %s WHERE idEstadio = %s",(porcentajeLLeno, idEstadio))
    db.commit()

#Insertamos los datos de la lista en la BBDD
def insertarAsistenteBaseDatos(listaAsistentes):
    
    db = establecerConexion()
    cursor = db.cursor()
    
    for asistente in listaAsistentes:
        sql = """INSERT INTO `asistente` (idEstadio, Nombre, 
        Apellido, Edad, DNI, PlazaEstadio) values(%s, %s, %s, %s, %s, %s)"""
        cursor.execute(sql, (asistente.idEstadio, asistente.nombre, asistente.apellido, asistente.edad, asistente.DNI, asistente.plazaEstadio))
        db.commit()

    for id in idEstadios:
        modificarPorcentajeLleno(id[0])

    return 

#Eliminamos lista de plazas de estadio de la BBDD 
def eliminarAsistentesBaseDatos(listaAsistentes):
    
    db = establecerConexion()
    cursor = db.cursor()
    
    for asistente in listaAsistentes:
        cursor.execute("DELETE FROM tfg.asistente WHERE PlazaEstadio = %s", asistente)
        db.commit()

    for id in idEstadios:
        modificarPorcentajeLleno(id[0])

    return 
