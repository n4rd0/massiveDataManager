"""

Desde esta ventana manejaremos la interfaz grafica de la aplicacion

"""

from tkinter import *  
import tkinter.messagebox
from Conector import establecerConexion
from EAI import correrSimulacion
from  threading import *
from GeneradorEstadios import generarEstadio 
import time

#Metricas globales

def obtenerMetricas():
    with open("metadata\MetricasSimulacion", 'r') as f:
        for data in f.readlines():
            
            if data.rsplit("=")[0] == "asistentesAGenerar":
                asistentesAGenerar = int(data.rsplit("=")[1])

            elif data.rsplit("=")[0] == "asistentesAEliminar":
                asistentesAEliminar = int(data.rsplit("=")[1])

            elif data.rsplit("=")[0] == "hilosAUsar":
                hilosAUsar = int(data.rsplit("=")[1])

            elif data.rsplit("=")[0] == "numeroDeEjecuciones":
                numeroDeEjecuciones = int(data.rsplit("=")[1])

            elif data.rsplit("=")[0] == "trabajoConHilos":
                if data.rsplit("=")[1] == "True\n":
                    trabajoConHilos = True
                else:
                    trabajoConHilos = False

    return (asistentesAGenerar,asistentesAEliminar,hilosAUsar,trabajoConHilos,numeroDeEjecuciones)

#Actualizamos las metricas de la simulacion accediendo al archivo local
def actualizarMetricasMetaData(asistentesAGenerar,asistentesAEliminar,hilosAUsar,trabajoConHilos,numeroDeEjecuciones):


        if asistentesAGenerar >=0 and asistentesAEliminar >= 0 and hilosAUsar >= 0 and numeroDeEjecuciones >= 0 and isinstance(asistentesAGenerar, int) and isinstance(asistentesAEliminar, int) and isinstance(numeroDeEjecuciones , int) and isinstance(hilosAUsar, int):

            with open("metadata\MetricasSimulacion", 'w') as f:
                f.write("asistentesAGenerar="+str(asistentesAGenerar)+"\n")
                f.write("asistentesAEliminar="+str(asistentesAEliminar)+"\n")
                f.write("hilosAUsar="+str(hilosAUsar)+"\n")
                f.write("trabajoConHilos="+str(trabajoConHilos)+"\n")
                f.write("numeroDeEjecuciones="+str(numeroDeEjecuciones)+"\n")
                tkinter.messagebox.showinfo("Notificacion Actualizar Metricas",  "Las metricas han sido actualizadas correctamente.")

        else:
            tkinter.messagebox.showinfo("Notificacion Actualizar Metricas",  "Error actualizando las metricas, revisa que los datos introducidos sean validos.")


pantallaDeInicio = Tk()
pantallaDeInicio.title("Massive Data Manager")
pantallaDeInicio.geometry("900x450")
pantallaDeInicio.resizable(False, False)

asistentesAGenerar, asistentesAEliminar, hilosAUsar, trabajoConHilos,numeroDeEjecuciones = obtenerMetricas()

#Funciones


#Devuelve los estadios en la bbdd
def obtenerListaDeEstadios():

    db = establecerConexion()
    cursor = db.cursor()

    cursor.execute("SELECT NombreEstadio FROM tfg.estadio")
    listaEstadios = cursor.fetchall()
    return listaEstadios

#Volver a la ventana principal
def abrirVentanaPrincipal(ventanaActual):
    asistentesAGenerar, asistentesAEliminar, hilosAUsar, trabajoConHilos,numeroDeEjecuciones = obtenerMetricas()

    ventanaActual.destroy()
    pantallaDeInicio = Tk()
    pantallaDeInicio.title("Massive Data Manager")
    pantallaDeInicio.geometry("900x450")
    pantallaDeInicio.resizable(False, False)

    #Visualizacion - Pantalla Principal


    tituloPantallaPrincipal = Label(pantallaDeInicio, text="Bienvenido, selecciona una de las siguientes opciones.", font=("InputMonoCondensed","20"))

    marcoContenedorOpcionesPantallaPrincipal = LabelFrame(pantallaDeInicio)

    textoVisualizacionDeEstadiosEnTiempoReal = Label(marcoContenedorOpcionesPantallaPrincipal, text="- Visualizacion de Estadios en Tiempo Real.", font=("InputMonoCondensed  18"))
    botonVisualizacionDeEstadiosEnTiempoReal = Button(marcoContenedorOpcionesPantallaPrincipal, width=6, height=1, 
        text="Acceso", font="InputMonoCondensed 12", command= lambda: abrirVisualizacionDeEstadiosEnTiempoReal(pantallaDeInicio))

    textoMetricasDeEstadiosEnTiempoReal = Label(marcoContenedorOpcionesPantallaPrincipal, compound= LEFT, text="- Metricas de Estadios en Tiempo Real.", font=("InputMonoCondensed  18"))
    botonMetricasDeEstadiosEnTiempoReal = Button(marcoContenedorOpcionesPantallaPrincipal, compound= LEFT, width=6, height=1, 
        text="Acceso", font="InputMonoCondensed 12", command= lambda:abrirVisualizacionMetricasDeEstadiosEnTiempoReal(pantallaDeInicio))

    textoConsultarEstadios = Label(marcoContenedorOpcionesPantallaPrincipal, text="- Consultar Estadios.", font=("InputMonoCondensed  18"))
    botonConsultarEstadios = Button(marcoContenedorOpcionesPantallaPrincipal, width=6, height=1, 
        text="Acceso", font="InputMonoCondensed 12", command= lambda:consultarEstadios(pantallaDeInicio))

    textoConsultarAsistentes = Label(marcoContenedorOpcionesPantallaPrincipal, text="- Consultar Asistentes.", font=("InputMonoCondensed  18"))
    botonConsultarAsistentes = Button(marcoContenedorOpcionesPantallaPrincipal, width=6, height=1, 
        text="Acceso", font="InputMonoCondensed 12", command= lambda:consultarAsistentes(pantallaDeInicio))


    textoCrearEstadio = Label(marcoContenedorOpcionesPantallaPrincipal, text="- Crear Nuevos Estadios.", font=("InputMonoCondensed  18"))
    botonCrearEstadio = Button(marcoContenedorOpcionesPantallaPrincipal, width=6, height=1, 
        text="Acceso", font="InputMonoCondensed 12", command= lambda:crearEstadio(pantallaDeInicio))

    textoAjustesMetricasSimulacion = Label(marcoContenedorOpcionesPantallaPrincipal, text="- Ajustes Metricas Simulacion.", font=("InputMonoCondensed  18"))
    botonAjustesMetricasSimulacion = Button(marcoContenedorOpcionesPantallaPrincipal, width=6, height=1, 
        text="Acceso", font="InputMonoCondensed 12", command= lambda:ajustesMetricasSimulacion(pantallaDeInicio))

    #Grid - Pantalla Principal

    tituloPantallaPrincipal.grid(row=0, column=0,pady=10, padx=40)

    marcoContenedorOpcionesPantallaPrincipal.grid(row=1, column=0, pady=10, padx=40)

    textoVisualizacionDeEstadiosEnTiempoReal.grid(row=2, column=0, pady=10, padx = 18)
    botonVisualizacionDeEstadiosEnTiempoReal.grid(row=2,column=1, padx=48, pady=10)

    textoMetricasDeEstadiosEnTiempoReal.grid(row=3, column=0, sticky= "w", padx= 18, pady=10)
    botonMetricasDeEstadiosEnTiempoReal.grid(row=3,column=1, padx=48, pady=10)

    textoConsultarEstadios.grid(row=4, column=0, sticky= "w", padx= 18, pady=10)
    botonConsultarEstadios.grid(row=4,column=1, padx=48, pady=10)

    textoConsultarAsistentes.grid(row=5, column=0, sticky= "w", padx= 18, pady=10)
    botonConsultarAsistentes.grid(row=5,column=1, padx=48, pady=10)

    textoCrearEstadio.grid(row=6, column=0, sticky= "w", padx= 18, pady=10)
    botonCrearEstadio.grid(row=6,column=1, padx=48, pady=10)

    textoAjustesMetricasSimulacion.grid(row=7, column=0, sticky= "w", padx= 18, pady=10)
    botonAjustesMetricasSimulacion.grid(row=7,column=1, padx=48, pady=10)
    
    pantallaDeInicio.mainloop()

#Cambia la ventana a la visualiacion de estadios en tiempo real
def abrirVisualizacionDeEstadiosEnTiempoReal(ventanaActual):
    #Clase de botones encargados de ejecutare el dibujo del estadio
    asistentesAGenerar, asistentesAEliminar, hilosAUsar, trabajoConHilos,numeroDeEjecuciones = obtenerMetricas()
    class botonEstadio():
        nombre = ""
        boton = None
    
        def __init__(self, nombre):
            self.nombre = nombre
            self.boton = Button(text=nombre, width=30, height=1, font="InputMonoCondensed 10", command= lambda:dibujarEstadio(nombre))

    #Eliminamos la ventana principal
    ventanaActual.destroy()

    #Configuracion de la ventana de visualizacion de estadios en tiempo real
    visualizacionDeEstadiosEnTiempoReal = Tk()
    visualizacionDeEstadiosEnTiempoReal.title("Visualizacion de Estadios en Tiempo Real")
    visualizacionDeEstadiosEnTiempoReal.geometry("1080x720")
    visualizacionDeEstadiosEnTiempoReal.resizable(False, False)

    estadios = obtenerListaDeEstadios()

    #Visualizacion - Pantalla Visualizacion de Estadios en Tiempo Real

    tituloPantallaDeVisualizacionDeEstadiosEnTiempoReal = Label(visualizacionDeEstadiosEnTiempoReal, 
    text="Bienvenido, selecciona un Estadio:", font=("InputMonoCondensed","10"))

    botonRegresoPantallaPrincipal = Button(visualizacionDeEstadiosEnTiempoReal, width=6, height=1,text="Home", 
    font="InputMonoCondensed 12", command= lambda: abrirVentanaPrincipal(visualizacionDeEstadiosEnTiempoReal))

    botonIniciarSimulacion = Button(visualizacionDeEstadiosEnTiempoReal, width=19, height=1,text="Empezar Simulacion", 
    font="InputMonoCondensed 12", command = lambda: correrSimulacionThreading(asistentesAGenerar, asistentesAEliminar, hilosAUsar, True, False, trabajoConHilos, numeroDeEjecuciones))

    frameCajaEstadio = LabelFrame(visualizacionDeEstadiosEnTiempoReal)
    global textoEstadio 
    textoEstadio = Text(frameCajaEstadio, width=90, height=35)

    #Funcion que nos permite dibujar el estadio seleccionado en la ventana
        
    def dibujarEstadio(nombreEstadio):
            global estadioSeleccionadoGlobal 
            estadioSeleccionadoGlobal = nombreEstadio

            db = establecerConexion()
            cursor = db.cursor()

            cursor.execute("SELECT idEstadio FROM tfg.estadio WHERE nombreEstadio = %s",nombreEstadio)
            idEstadio = cursor.fetchall()[0][0]

            cursor.execute("SELECT PlazaEstadio FROM tfg.asistente WHERE idEstadio = %s",idEstadio)
            plazas = cursor.fetchall()
            plazasOcupadas = []
            for p in plazas:
                plazasOcupadas.append(p[0])

            cursor.execute("SELECT Secciones, Grupos, Filas, Asientos FROM tfg.estadio WHERE NombreEstadio = %s",nombreEstadio)

            infoAsientosEstadio = cursor.fetchall()

            textoEstadio.delete(1.0,END)

            cursor.execute("SELECT PorcentajeLLeno FROM tfg.estadio WHERE NombreEstadio = %s",nombreEstadio)
            porcentajeDeLlenado = cursor.fetchall()[0][0]

            textoEstadio.insert(END,nombreEstadio+" Porcentaje de Llenado: "+str(round(porcentajeDeLlenado,2))+"%\n\n")

            for i in range(1,infoAsientosEstadio[0][0]+1):
                textoEstadio.insert(END, "Seccion: "+str(i)+"\n")
                for j in range(1,infoAsientosEstadio[0][1]+1):

                    textTemp = Text(width= 9,height=4, font="InputMonoCondensed 6")
                    textoEstadio.window_create(END,window=textTemp)

                    for k in range(1,infoAsientosEstadio[0][2]+1):
                        for l in range(1,infoAsientosEstadio[0][3]+1):

                            seccion = "0"+str(i)
                            seccion = seccion[-2:]

                            grupo = "0"+str(j)
                            grupo = grupo[-2:]

                            fila = "0"+str(k)
                            fila = fila[-2:]

                            asiento = "0"+str(l)
                            asiento = asiento[-2:]

                            colorDelFondo = "green"
                            if seccion+grupo+fila+asiento in plazasOcupadas:
                                colorDelFondo = "red"

                            textTemp2 = Text(bg = colorDelFondo, width= 1,height=1, font="InputMonoCondensed 6")
                            textTemp.window_create(END,window=textTemp2)

                textoEstadio.insert(END,"\n")
                textoEstadio.insert(END,"\n")
            time.sleep(2)
    
    def dibujarEstadioAux(hiloEjecucion):
        while(hiloEjecucion.is_alive()):
            try:
                t1 = Thread(target=dibujarEstadio,args=(estadioSeleccionadoGlobal,))
                t1.start()
                
                t1.join()
            except:
                continue
        tkinter.messagebox.showinfo("Notificacion Simulacion",  "Simulacion Finalizada Con Exito.")

    #Funcion que en otro hilo ejecuta la simulacion para no crashear el programa principal
    def correrSimulacionThreading(asistentesAGenerar, asistentesAEliminar, hilosAUsar, generarSubida, imprimirPorPantalla, trabajoConHilos, numeroDeEjecuciones):
        t1 = Thread(target=correrSimulacion, args = (asistentesAGenerar, asistentesAEliminar, hilosAUsar, generarSubida, imprimirPorPantalla, trabajoConHilos, numeroDeEjecuciones, ))
        botonIniciarSimulacion["state"] = DISABLED
        t1.start()
        t2 = Thread(target=dibujarEstadioAux, args=(t1,))
        t2.start()
        botonIniciarSimulacion["state"] = NORMAL
        dibujarEstadio(estadioSeleccionadoGlobal)

    frameCajaScrollConEstadios = LabelFrame(visualizacionDeEstadiosEnTiempoReal)
    texto = Text(frameCajaScrollConEstadios, width=28, height=35)
    cajaScrolleableConEstadios = Scrollbar(frameCajaScrollConEstadios, command=texto.yview)
    texto.configure(yscrollcommand=cajaScrolleableConEstadios.set)

    dictBotones = {}
    for estadio in estadios:
        dictBotones["boton {0}".format(estadio[0])] = botonEstadio(estadio[0])
    
    for b in dictBotones.values():
        texto.window_create(END, window=b.boton)
        texto.insert(END,"\n")

    texto.configure(state=DISABLED)

    #Grid - Pantalla Visualizacion de Estadios en Tiempo Real

    tituloPantallaDeVisualizacionDeEstadiosEnTiempoReal.grid(row=0,column=0, pady=10, sticky="w", padx=15)
    botonRegresoPantallaPrincipal.grid(row=0,column=1, pady=10, padx=10, sticky="e")

    frameCajaScrollConEstadios.grid(row = 1, column=0, pady=10, padx=15)
    texto.pack(side=LEFT, pady=10, padx = 10)
    cajaScrolleableConEstadios.pack(side=RIGHT, fill=Y, pady=10,padx=10)

    frameCajaEstadio.grid(row = 1, column=1, pady=10,padx=10, sticky="w")
    textoEstadio.grid(row=0, column=0)

    botonIniciarSimulacion.grid(row = 2, column = 1, pady=10,padx=10, sticky="e")

    visualizacionDeEstadiosEnTiempoReal.mainloop()

#Cambia la ventana a la visualiacion de metricas de estadios en tiempo real
def abrirVisualizacionMetricasDeEstadiosEnTiempoReal(ventanaActual):
    #Clase de botones encargados de ejecutare el dibujo del estadio
    asistentesAGenerar, asistentesAEliminar, hilosAUsar, trabajoConHilos,numeroDeEjecuciones = obtenerMetricas()
    class botonEstadio():
        nombre = ""
        boton = None
    
        def __init__(self, nombre):
            self.nombre = nombre
            self.boton = Button(text=nombre, width=30, height=1, font="InputMonoCondensed 10", command= lambda:dibujarMetricas(nombre))
    #Eliminamos la ventana principal
    ventanaActual.destroy()

    #Configuracion de la ventana de visualizacion de estadios en tiempo real
    visualizacionDeMetricasDeEstadiosEnTiempoReal = Tk()
    visualizacionDeMetricasDeEstadiosEnTiempoReal.title("Visualizacion de Metricas de Estadios en Tiempo Real")
    visualizacionDeMetricasDeEstadiosEnTiempoReal.geometry("1080x720")
    visualizacionDeMetricasDeEstadiosEnTiempoReal.resizable(False, False)

    estadios = obtenerListaDeEstadios()

    #Visualizacion - Pantalla Visualizacion de Estadios en Tiempo Real

    tituloPantallaDeVisualizacionDeEstadiosEnTiempoReal = Label(visualizacionDeMetricasDeEstadiosEnTiempoReal, 
    text="Bienvenido, selecciona un Estadio:", font=("InputMonoCondensed","10"))

    botonRegresoPantallaPrincipal = Button(visualizacionDeMetricasDeEstadiosEnTiempoReal, width=6, height=1,text="Home", 
    font="InputMonoCondensed 12", command= lambda: abrirVentanaPrincipal(visualizacionDeMetricasDeEstadiosEnTiempoReal))

    botonIniciarSimulacion = Button(visualizacionDeMetricasDeEstadiosEnTiempoReal, width=19, height=1,text="Empezar Simulacion", 
    font="InputMonoCondensed 12", command = lambda: correrSimulacionThreading(asistentesAGenerar, asistentesAEliminar, hilosAUsar, True, False, trabajoConHilos, numeroDeEjecuciones))

    frameCajaEstadio = LabelFrame(visualizacionDeMetricasDeEstadiosEnTiempoReal)
    textoEstadio = Text(frameCajaEstadio, width=90, height=35)

    #Funcion que nos permite dibujar el estadio seleccionado en la ventana
        
    def dibujarMetricas(nombreEstadio):
            db = establecerConexion()
            cursor = db.cursor()

            cursor.execute("SELECT * FROM tfg.estadio")
            metricas = cursor.fetchall()

            textoEstadio.delete(1.0,END)

            for metrica in metricas:
                if nombreEstadio in metrica:
                    metricasEstadioSeleccionado = metrica

            textoEstadio.insert(END,nombreEstadio+"\n")
            textoEstadio.insert(END,"Capacidad: "+str(metricasEstadioSeleccionado[2])+"\n")
            textoEstadio.insert(END,"Ubicacion: "+str(metricasEstadioSeleccionado[3])+"\n")
            textoEstadio.insert(END,"Secciones: "+str(metricasEstadioSeleccionado[4])+"\n")
            textoEstadio.insert(END,"Grupos: "+str(metricasEstadioSeleccionado[5])+"\n")
            textoEstadio.insert(END,"Filas: "+str(metricasEstadioSeleccionado[6])+"\n")
            textoEstadio.insert(END,"Asientos: "+str(metricasEstadioSeleccionado[7])+"\n")
            textoEstadio.insert(END,"Porcentaje Lleno: "+str(round(metricasEstadioSeleccionado[8],4))+"%\n")
 
    #Funcion que en otro hilo ejecuta la simulacion para no crashear el programa principal
    def correrSimulacionThreading(asistentesAGenerar, asistentesAEliminar, hilosAUsar, generarSubida, imprimirPorPantalla, trabajoConHilos, numeroDeEjecuciones):
        t1 = Thread(target=correrSimulacion, args = (asistentesAGenerar, asistentesAEliminar, hilosAUsar, generarSubida, imprimirPorPantalla, trabajoConHilos, numeroDeEjecuciones, ))
        botonIniciarSimulacion["state"] = DISABLED
        t1.start()
        botonIniciarSimulacion["state"] = NORMAL
    
    frameCajaScrollConEstadios = LabelFrame(visualizacionDeMetricasDeEstadiosEnTiempoReal)
    texto = Text(frameCajaScrollConEstadios, width=28, height=35)
    cajaScrolleableConEstadios = Scrollbar(frameCajaScrollConEstadios, command=texto.yview)
    texto.configure(yscrollcommand=cajaScrolleableConEstadios.set)

    dictBotones = {}
    for estadio in estadios:
        dictBotones["boton {0}".format(estadio[0])] = botonEstadio(estadio[0])
    
    for b in dictBotones.values():
        texto.window_create(END, window=b.boton)
        texto.insert(END,"\n")

    texto.configure(state=DISABLED)

    #Grid - Pantalla Visualizacion de Estadios en Tiempo Real

    tituloPantallaDeVisualizacionDeEstadiosEnTiempoReal.grid(row=0,column=0, pady=10, sticky="w", padx=15)
    botonRegresoPantallaPrincipal.grid(row=0,column=1, pady=10, padx=10, sticky="e")

    frameCajaScrollConEstadios.grid(row = 1, column=0, pady=10, padx=15)
    texto.pack(side=LEFT, pady=10, padx = 10)
    cajaScrolleableConEstadios.pack(side=RIGHT, fill=Y, pady=10,padx=10)

    frameCajaEstadio.grid(row = 1, column=1, pady=10,padx=10, sticky="w")
    textoEstadio.grid(row=0, column=0)

    botonIniciarSimulacion.grid(row = 2, column = 1, pady=10,padx=10, sticky="e")

    visualizacionDeMetricasDeEstadiosEnTiempoReal.mainloop()

#Lista de los estadios registrados en el sistema
def consultarEstadios(ventanaActual):
    asistentesAGenerar, asistentesAEliminar, hilosAUsar, trabajoConHilos,numeroDeEjecuciones = obtenerMetricas()

    estadioSeleccionado = ""

    def updateListBox(lista):
        textoEstadio.delete(0,END)

        for l in lista:
            textoEstadio.insert(END,l)
    
    def check(e):
        typed = barraDeBusqueda.get()

        if typed =='':
            data = nombresEstadios
        else:
            data = []
            for item in nombresEstadios:
                if typed.lower() in item.lower():
                    data.append(item)
        
        updateListBox(data)

    ventanaActual.destroy()

    visualizacionConsultarEstadios = Tk()
    visualizacionConsultarEstadios.title("Consultar Estadios")
    visualizacionConsultarEstadios.geometry("1080x720")
    visualizacionConsultarEstadios.resizable(False, False)

    tituloPantallaDeVisualizacionDeEstadiosEnTiempoReal = Label(visualizacionConsultarEstadios, 
    text="Bienvenido, introduce el estadio que quieres buscar en la barra de navegacion:", font=("InputMonoCondensed","10"))

    botonRegresoPantallaPrincipal = Button(visualizacionConsultarEstadios, width=6, height=1,text="Home", 
    font="InputMonoCondensed 12", command= lambda: abrirVentanaPrincipal(visualizacionConsultarEstadios))


    frameCajaEstadio = LabelFrame(visualizacionConsultarEstadios)
    barraDeBusqueda = Entry(frameCajaEstadio, font="InputMonoCondensed 12", width=60)
    textoEstadio = Listbox(frameCajaEstadio, width=90, height=30)
    eliminarEstadioBoton = Button(frameCajaEstadio, width=20, height=1,text="Eliminar Estadio", 
        font="InputMonoCondensed 12", command= lambda: eliminarEstadioSeleccionado())
    
    def fillout(e):
            estadioSeleccionado = textoEstadio.get(textoEstadio.curselection())
            return estadioSeleccionado

    barraDeBusqueda.bind("<KeyRelease>", check)
    textoEstadio.bind("<<ListboxSelect>>", fillout)

    listaEstadios = obtenerListaDeEstadios()
    nombresEstadios = []
    for estadio in listaEstadios:
        nombresEstadios.append(estadio[0])
    
    updateListBox(nombresEstadios)

    def eliminarEstadioSeleccionado():

        estadioSeleccionado = fillout("<<ListboxSelect>>")
        db = establecerConexion()
        cursor = db.cursor()

        cursor.execute("SELECT idEstadio FROM tfg.estadio WHERE NombreEstadio = %s", estadioSeleccionado)
        idEstadio = cursor.fetchall()[0][0]
        cursor.execute("DELETE FROM tfg.asistente WHERE idEstadio = %s", idEstadio)
        db.commit()
        cursor.execute("DELETE FROM tfg.estadio WHERE NombreEstadio = %s", estadioSeleccionado)
        db.commit()

        nombresEstadios.remove(estadioSeleccionado)
        updateListBox(nombresEstadios)

    #Grid - Pantalla Visualizacion de Estadios en Tiempo Real

    tituloPantallaDeVisualizacionDeEstadiosEnTiempoReal.grid(row=0,column=0, pady=10, sticky="w", padx=240)
    botonRegresoPantallaPrincipal.grid(row=2,column=0, pady=10, padx=10)

    frameCajaEstadio.grid(row = 1, column=0, pady=10,padx=240, sticky="w")
    barraDeBusqueda.grid(row=0,column=0, pady=10)
    textoEstadio.grid(row=1, column=0, pady=10)
    eliminarEstadioBoton.grid(row=2, column=0, pady=10)

    visualizacionConsultarEstadios.mainloop()

#Lista de los asistentes con su respectivo estadio en el sistema
def consultarAsistentes(ventanaActual):
    asistentesAGenerar, asistentesAEliminar, hilosAUsar, trabajoConHilos,numeroDeEjecuciones = obtenerMetricas()

    def updateListBox(lista, limit):
        textoAsistente.delete(0,END)

        for l in lista:
            if limit == 0:
                break
            textoAsistente.insert(END,l)
            limit -=1
    
    def check(e):
        typed = barraDeBusqueda.get()

        if typed =='':
            data = asistentes
        else:
            data = []
            for item in asistentes:
                if typed.lower() in item.lower():
                    data.append(item)
        
        updateListBox(data,1000)

    ventanaActual.destroy()

    visualizacionConsultarAsistentes = Tk()
    visualizacionConsultarAsistentes.title("Consultar Asistentes")
    visualizacionConsultarAsistentes.geometry("1080x720")
    visualizacionConsultarAsistentes.resizable(False, False)

    tituloPantallaDeVisualizacionDeEstadiosEnTiempoReal = Label(visualizacionConsultarAsistentes, 
    text="Bienvenido, introduce el estadio que quieres buscar en la barra de navegacion:", font=("InputMonoCondensed","10"))

    botonRegresoPantallaPrincipal = Button(visualizacionConsultarAsistentes, width=6, height=1,text="Home", 
    font="InputMonoCondensed 12", command= lambda: abrirVentanaPrincipal(visualizacionConsultarAsistentes))


    frameCajaEstadio = LabelFrame(visualizacionConsultarAsistentes)
    barraDeBusqueda = Entry(frameCajaEstadio, font="InputMonoCondensed 12", width=60)
    textoAsistente = Listbox(frameCajaEstadio, width=90, height=30)


    db = establecerConexion()
    cursor = db.cursor()

    cursor.execute("SELECT * from tfg.asistente")

    listaDeAsistentes = cursor.fetchall()
    asistentes = []

    for asistente in listaDeAsistentes:

        cursor.execute("SELECT NombreEstadio FROM tfg.estadio WHERE idEstadio = %s",asistente[1])
        estadio = cursor.fetchall()[0][0]

        asistentes.append(str(asistente[0])+"    Estadio: "+estadio+"    Nombre y Apellido: "+asistente[2]+" "+asistente[3]+"    DNI: "+asistente[5])
    
    updateListBox(asistentes,1000)

    barraDeBusqueda.bind("<KeyRelease>", check)

    #Grid - Pantalla Visualizacion de Estadios en Tiempo Real

    tituloPantallaDeVisualizacionDeEstadiosEnTiempoReal.grid(row=0,column=0, pady=10, sticky="w", padx=240)
    botonRegresoPantallaPrincipal.grid(row=2,column=0, pady=10, padx=10)

    frameCajaEstadio.grid(row = 1, column=0, pady=10,padx=240, sticky="w")
    barraDeBusqueda.grid(row=0,column=0, pady=10)
    textoAsistente.grid(row=1, column=0, pady=10)

    visualizacionConsultarAsistentes.mainloop()
    
#Crear estadios
def crearEstadio(ventanaActual): 
    asistentesAGenerar, asistentesAEliminar, hilosAUsar, trabajoConHilos,numeroDeEjecuciones = obtenerMetricas()

    def generarEstadioAux():
        
        try:
            NombreEstadio = entryNombreEstadio.get()
            Ubicacion = entryUbicacionEstadio.get()
            Secciones = entrySeccionesEstadio.get() 
            Grupos = entryGruposEstadio.get() 
            Filas = entryFilasEstadio.get() 
            Asientos = entryAsientosEstadio.get()
            Secciones = int(Secciones)
            Grupos = int(Grupos)
            Filas = int(Filas)
            Asientos = int(Asientos)

            if isinstance(Secciones, int) and Secciones > 0 and isinstance(Grupos, int) and Grupos > 0 and isinstance(Filas, int) and Filas > 0 and isinstance(Asientos, int) and Asientos > 0 and NombreEstadio.strip() != "" and Ubicacion.strip() != "":
                tkinter.messagebox.showinfo("Notificacion Crear Estadio",  "El Estadio se ha creado Correctamente")
                generarEstadio(NombreEstadio, Ubicacion, Secciones, Grupos,Filas, Asientos)
            
            else:
                tkinter.messagebox.showinfo("Notificacion Crear Estadio",  "Los datos introducidos son incorrectos. Revisalos y vuelve a introducirlos")
        except ValueError:
            tkinter.messagebox.showinfo("Notificacion Crear Estadio",  "Los datos introducidos son incorrectos. Revisalos y vuelve a introducirlos")

    ventanaActual.destroy()

    visualizacionCrearEstadio = Tk()
    visualizacionCrearEstadio.title("Crear Estadio")
    visualizacionCrearEstadio.geometry("1080x500")
    visualizacionCrearEstadio.resizable(False, False)

    tituloPantallaDeVisualizacionDeEstadiosEnTiempoReal = Label(visualizacionCrearEstadio, 
    text="Bienvenido, introduce las metricas deseadas para la generacion de su estadio:", font=("InputMonoCondensed","10"))
    
    frameCajaEstadio = LabelFrame(visualizacionCrearEstadio)

    listaDeEntrys = []

    nombreEstadio = Label(frameCajaEstadio, font="InputMonoCondensed 10", width=60,text="Nombre del Estadio:")
    entryNombreEstadio = Entry(frameCajaEstadio, font="InputMonoCondensed 10", width=60)
    listaDeEntrys.append(entryNombreEstadio)

    ubicacionEstadio = Label(frameCajaEstadio, font="InputMonoCondensed 10", width=60,text="Ubicacaion del Estadio:")
    entryUbicacionEstadio = Entry(frameCajaEstadio, font="InputMonoCondensed 10", width=60)
    listaDeEntrys.append(entryUbicacionEstadio)

    seccionesEstadio = Label(frameCajaEstadio, font="InputMonoCondensed 10", width=60,text="Introduzca el numero de Secciones del Estadio:")
    entrySeccionesEstadio = Entry(frameCajaEstadio, font="InputMonoCondensed 10", width=60)
    listaDeEntrys.append(entrySeccionesEstadio)

    gruposEstadio = Label(frameCajaEstadio, font="InputMonoCondensed 10", width=60,text="Introduzca el numero de Grupos por Seccion:")
    entryGruposEstadio = Entry(frameCajaEstadio, font="InputMonoCondensed 10", width=60)
    listaDeEntrys.append(entryGruposEstadio)


    filasEstadio = Label(frameCajaEstadio, font="InputMonoCondensed 10", width=60,text="Introduzca el numero de Filas por Grupo:")
    entryFilasEstadio = Entry(frameCajaEstadio, font="InputMonoCondensed 10", width=60)
    listaDeEntrys.append(entryFilasEstadio)


    asientosEstadio = Label(frameCajaEstadio, font="InputMonoCondensed 10", width=60,text="Introduzca el numero de Asientos que por Fila:")
    entryAsientosEstadio = Entry(frameCajaEstadio, font="InputMonoCondensed 10", width=60)
    listaDeEntrys.append(entryAsientosEstadio)

    crearEstadioBoton = Button(frameCajaEstadio, width=17, height=1,text="Generar Estadio", 
    font="InputMonoCondensed 12", command= lambda: generarEstadioAux())

    botonRegresoPantallaPrincipal = Button(visualizacionCrearEstadio, width=6, height=1,text="Home", 
    font="InputMonoCondensed 12", command= lambda: abrirVentanaPrincipal(visualizacionCrearEstadio))

    #Grid - Pantalla Visualizacion de Estadios en Tiempo Real

    tituloPantallaDeVisualizacionDeEstadiosEnTiempoReal.grid(row=0,column=0, pady=10, sticky="w", padx=100)

    frameCajaEstadio.grid(row = 1, column=0, pady=10,padx=100, sticky="w")
   
    nombreEstadio.grid(row=0,column=0, pady=10)
    entryNombreEstadio.grid(row=0,column=1, pady=10, padx = 20)
    
    ubicacionEstadio.grid(row=1, column=0, pady=10)
    entryUbicacionEstadio.grid(row=1, column=1, pady=10, padx = 20)

    seccionesEstadio.grid(row=2,column=0, pady=10)
    entrySeccionesEstadio.grid(row=2,column=1, pady=10, padx = 20)

    gruposEstadio.grid(row=3,column=0, pady=10)
    entryGruposEstadio.grid(row=3,column=1, pady=10, padx = 20)

    filasEstadio.grid(row=4,column=0, pady=10)
    entryFilasEstadio.grid(row=4,column=1, pady=10, padx = 20)

    asientosEstadio.grid(row=5,column=0, pady=10)
    entryAsientosEstadio.grid(row=5,column=1, pady=10, padx = 20)

    crearEstadioBoton.grid(row=6,columnspan=2, pady = 10)

    botonRegresoPantallaPrincipal.grid(row=2,column=0, pady=10, padx=10)

    visualizacionCrearEstadio.mainloop()

#Permite ajustar las metricas de la simulacion
def ajustesMetricasSimulacion(ventanaActual):

    def actualizarMetricas():

        tuplaMetricas = obtenerMetricas()

        entryAsistentesAGenerar.insert(END,str(tuplaMetricas[0]))
        entryAsistentesAEliminar.insert(END,str(tuplaMetricas[1]))
        entryhilosAUsar.insert(END, str(tuplaMetricas[2]))
        entryNumeroDeEjecuciones.insert(END,tuplaMetricas[4])
        if tuplaMetricas[3]:
            entrytrabajarConHilos.setvar("checkMarcado",1)
        else: 
            entrytrabajarConHilos.setvar("checkMarcado",0)

    def cambiarMetricas():

        try:
        
            asistentesAGenerar = int(entryAsistentesAGenerar.get())
            asistentesAEliminar = int(entryAsistentesAEliminar.get())
            hilosAUsar = int(entryhilosAUsar.get())
            numeroDeEjecuciones = int(entryNumeroDeEjecuciones.get())

            trabajoConHilos = int(entrytrabajarConHilos.getvar("checkMarcado"))
            if trabajoConHilos == 1:
                trabajoConHilos = True
            else:
                trabajoConHilos = False

            actualizarMetricasMetaData(asistentesAGenerar,asistentesAEliminar,hilosAUsar,trabajoConHilos,numeroDeEjecuciones)

        except:
            tkinter.messagebox.showinfo("Notificacion Actualizar Metricas",  "Error actualizando las metricas, revisa que los datos introducidos sean validos.")


    ventanaActual.destroy()

    visualizacionCambiarMetricas = Tk()
    visualizacionCambiarMetricas.title("Ajustes Metricas")
    visualizacionCambiarMetricas.geometry("1080x500")
    visualizacionCambiarMetricas.resizable(False, False)

    tituloPantallaDeVisualizacionDeEstadiosEnTiempoReal = Label(visualizacionCambiarMetricas, 
    text="Bienvenido, introduce las metricas deseadas para la generacion de su estadio:", font=("InputMonoCondensed","10"))
    
    frameCajaEstadio = LabelFrame(visualizacionCambiarMetricas)

    listaDeEntrys = []

    LabelasistentesAGenerar = Label(frameCajaEstadio, font="InputMonoCondensed 10", width=60,text="Asistentes a Generar por Ejecucion:")
    entryAsistentesAGenerar = Entry(frameCajaEstadio, font="InputMonoCondensed 10", width=60)
    listaDeEntrys.append(asistentesAGenerar)

    LabelasistentesAEliminar = Label(frameCajaEstadio, font="InputMonoCondensed 10", width=60,text="Asistentes a Eliminar por Ejecucion:")
    entryAsistentesAEliminar = Entry(frameCajaEstadio, font="InputMonoCondensed 10", width=60)
    listaDeEntrys.append(entryAsistentesAEliminar)

    LabelhilosAUsar = Label(frameCajaEstadio, font="InputMonoCondensed 10", width=60,text="Hilos a usar en la Ejecucion:")
    entryhilosAUsar = Entry(frameCajaEstadio, font="InputMonoCondensed 10", width=60)
    listaDeEntrys.append(entryhilosAUsar)

    LabeltrabajarConHilos = Label(frameCajaEstadio, font="InputMonoCondensed 10", width=60,text="Marque si desea trabajar en Multiprocesado:")
    entrytrabajarConHilos = Checkbutton(frameCajaEstadio, font="InputMonoCondensed 10", width=60, onvalue=1,offvalue=0, variable="checkMarcado")
    listaDeEntrys.append(entrytrabajarConHilos)

    LabelnumeroDeEjecuciones = Label(frameCajaEstadio, font="InputMonoCondensed 10", width=60,text="Numero de Ejecuciones:")
    entryNumeroDeEjecuciones = Entry(frameCajaEstadio, font="InputMonoCondensed 10", width=60)
    listaDeEntrys.append(entryNumeroDeEjecuciones)

    actualizarMetricasBoton = Button(frameCajaEstadio, width=20, height=1,text="Actualizar Metricas", 
    font="InputMonoCondensed 12", command= lambda: cambiarMetricas())

    botonRegresoPantallaPrincipal = Button(visualizacionCambiarMetricas, width=6, height=1,text="Home", 
    font="InputMonoCondensed 12", command= lambda: abrirVentanaPrincipal(visualizacionCambiarMetricas))

    actualizarMetricas()
    #Grid - Pantalla Visualizacion de Estadios en Tiempo Real

    tituloPantallaDeVisualizacionDeEstadiosEnTiempoReal.grid(row=0,column=0, pady=10, sticky="w", padx=100)

    frameCajaEstadio.grid(row = 1, column=0, pady=10,padx=100, sticky="w")
   
    LabelasistentesAGenerar.grid(row=0,column=0, pady=10)
    entryAsistentesAGenerar.grid(row=0,column=1, pady=10, padx = 20)
    
    LabelasistentesAEliminar.grid(row=1, column=0, pady=10)
    entryAsistentesAEliminar.grid(row=1, column=1, pady=10, padx = 20)

    LabelhilosAUsar.grid(row=2,column=0, pady=10)
    entryhilosAUsar.grid(row=2,column=1, pady=10, padx = 20)

    LabelnumeroDeEjecuciones.grid(row=3,column=0, pady=10)
    entryNumeroDeEjecuciones.grid(row=3,column=1, pady=10, padx = 20)

    LabeltrabajarConHilos.grid(row=4,column=0, pady=10)
    entrytrabajarConHilos.grid(row=4,column=1, pady=10, padx = 20)

    actualizarMetricasBoton.grid(row=6,columnspan=2, pady = 10)

    botonRegresoPantallaPrincipal.grid(row=2,column=0, pady=10, padx=10)

#Visualizacion - Pantalla Principal 
tituloPantallaPrincipal = Label(pantallaDeInicio, text="Bienvenido, selecciona una de las siguientes opciones.", font=("InputMonoCondensed","20"))

marcoContenedorOpcionesPantallaPrincipal = LabelFrame(pantallaDeInicio)

textoVisualizacionDeEstadiosEnTiempoReal = Label(marcoContenedorOpcionesPantallaPrincipal, text="- Visualizacion de Estadios en Tiempo Real.", font=("InputMonoCondensed  18"))
botonVisualizacionDeEstadiosEnTiempoReal = Button(marcoContenedorOpcionesPantallaPrincipal, width=6, height=1, 
    text="Acceso", font="InputMonoCondensed 12", command= lambda: abrirVisualizacionDeEstadiosEnTiempoReal(pantallaDeInicio))

textoMetricasDeEstadiosEnTiempoReal = Label(marcoContenedorOpcionesPantallaPrincipal, compound= LEFT, text="- Metricas de Estadios en Tiempo Real.", font=("InputMonoCondensed  18"))
botonMetricasDeEstadiosEnTiempoReal = Button(marcoContenedorOpcionesPantallaPrincipal, compound= LEFT, width=6, height=1, 
    text="Acceso", font="InputMonoCondensed 12", command= lambda:abrirVisualizacionMetricasDeEstadiosEnTiempoReal(pantallaDeInicio))

textoConsultarEstadios = Label(marcoContenedorOpcionesPantallaPrincipal, text="- Consultar Estadios.", font=("InputMonoCondensed  18"))
botonConsultarEstadios = Button(marcoContenedorOpcionesPantallaPrincipal, width=6, height=1, 
    text="Acceso", font="InputMonoCondensed 12", command= lambda:consultarEstadios(pantallaDeInicio))

textoConsultarAsistentes = Label(marcoContenedorOpcionesPantallaPrincipal, text="- Consultar Asistentes.", font=("InputMonoCondensed  18"))
botonConsultarAsistentes = Button(marcoContenedorOpcionesPantallaPrincipal, width=6, height=1, 
    text="Acceso", font="InputMonoCondensed 12", command= lambda:consultarAsistentes(pantallaDeInicio))


textoCrearEstadio = Label(marcoContenedorOpcionesPantallaPrincipal, text="- Crear Nuevos Estadios.", font=("InputMonoCondensed  18"))
botonCrearEstadio = Button(marcoContenedorOpcionesPantallaPrincipal, width=6, height=1, 
    text="Acceso", font="InputMonoCondensed 12", command= lambda:crearEstadio(pantallaDeInicio))

textoAjustesMetricasSimulacion = Label(marcoContenedorOpcionesPantallaPrincipal, text="- Ajustes Metricas Simulacion.", font=("InputMonoCondensed  18"))
botonAjustesMetricasSimulacion = Button(marcoContenedorOpcionesPantallaPrincipal, width=6, height=1, 
    text="Acceso", font="InputMonoCondensed 12", command= lambda:ajustesMetricasSimulacion(pantallaDeInicio))

#Grid - Pantalla Principal

tituloPantallaPrincipal.grid(row=0, column=0,pady=10, padx=40)

marcoContenedorOpcionesPantallaPrincipal.grid(row=1, column=0, pady=10, padx=40)

textoVisualizacionDeEstadiosEnTiempoReal.grid(row=2, column=0, pady=10, padx = 18)
botonVisualizacionDeEstadiosEnTiempoReal.grid(row=2,column=1, padx=48, pady=10)

textoMetricasDeEstadiosEnTiempoReal.grid(row=3, column=0, sticky= "w", padx= 18, pady=10)
botonMetricasDeEstadiosEnTiempoReal.grid(row=3,column=1, padx=48, pady=10)

textoConsultarEstadios.grid(row=4, column=0, sticky= "w", padx= 18, pady=10)
botonConsultarEstadios.grid(row=4,column=1, padx=48, pady=10)

textoConsultarAsistentes.grid(row=5, column=0, sticky= "w", padx= 18, pady=10)
botonConsultarAsistentes.grid(row=5,column=1, padx=48, pady=10)

textoCrearEstadio.grid(row=6, column=0, sticky= "w", padx= 18, pady=10)
botonCrearEstadio.grid(row=6,column=1, padx=48, pady=10)

textoAjustesMetricasSimulacion.grid(row=7, column=0, sticky= "w", padx= 18, pady=10)
botonAjustesMetricasSimulacion.grid(row=7,column=1, padx=48, pady=10)

pantallaDeInicio.mainloop()