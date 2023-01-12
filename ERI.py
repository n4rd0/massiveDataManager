import threading
from GeneradorHilos import * 

"""

Entidad Receptora de la informacion, nos permite generar asistentes para posteriormente estos ser pasados la EAI cuando sean solicitados

"""

def generarAsistentesERI(numeroDeAsistentes, numeroDeHilos, generarSubida, imprimirPorPantalla, trabajoConHilos):
    from  Generador import generarAsistentes, insertarAsistenteBaseDatos, actualizarPlazas
    actualizarPlazas()

    #Trabajando con el numero indicado de hilos
    if trabajoConHilos:
        t = []
        
        for _ in range(numeroDeHilos):
            th = threading.Thread(target = generarAsistentesHilo, args = (numeroDeAsistentes, generarSubida, imprimirPorPantalla, ))
            th.start()
            t.append(th)
            
        for thread in t:
            thread.join()
    #Trabajamos en single thread
    else:
        asistentes = generarAsistentes(numeroDeAsistentes)
        if imprimirPorPantalla:
            for asistente in asistentes: 
                print(asistente)
