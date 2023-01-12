import time 
from ERI import generarAsistentesERI
from Generador import eliminarAsistentes
from Conector import establecerConexion
import tkinter.messagebox

"""

La entidad actualizadora de la información será la encargada de periódicamente actualizar que asientos están ocupados de que estadios
e irá gestionando la información. 

"""

#Corre la simulacion de entrada y salida de asistentes a los teatros.
def correrSimulacion(asistentesAGenerar, asistentesAEliminar, hilosAUsar, generarSubida, imprimirPorPantalla, trabajoConHilos, numeroDeEjecuciones):
    while numeroDeEjecuciones > 0:
        db = establecerConexion()
        cursor = db.cursor()

        generarAsistentesERI(asistentesAGenerar, hilosAUsar,generarSubida, imprimirPorPantalla, trabajoConHilos)

        inicioEliminacion = time.time()

        nEstadios = cursor.execute("SELECT NombreEstadio FROM tfg.estadio WHERE PorcentajeLLeno > 0")
        estadios = cursor.fetchall()

        eliminarAsistentes(asistentesAEliminar)

        if trabajoConHilos:
                asistGenerados = asistentesAGenerar*hilosAUsar
        else: 
                asistGenerados = asistentesAGenerar

        print("\n--- Ejecucion Completada en %.4f s. Asistentes Generados: %i. ---" % (time.time() - inicioEliminacion, asistGenerados))
        print("\n--- Ejecucion Completada en %.4f s. Asistentes Eliminados: %i. ---" % (time.time() - inicioEliminacion, asistentesAEliminar))

        numeroDeEjecuciones-=1
        time.sleep(2)
