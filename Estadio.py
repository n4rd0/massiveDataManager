class Estadio: 
    
    #La PK de la bbdd se autoincrementa y no es parte del objeto
    def __init__ (self, nombreEstadio , capacidad, ubicacion, secciones, grupos, filas, asientos, 
                  porcentajeLleno):
        self.nombreEstadio = nombreEstadio
        self.capacidad = capacidad
        self.ubicacion = ubicacion
        self.secciones = secciones
        self.grupos = grupos
        self.filas = filas
        self.asientos = asientos
        self.porcentajeLleno = porcentajeLleno

    def __str__(self):
        
        return ("\nEstadio: {0} \nubicado en: {1} \ncapacidad: {2} asistentes").format(self.nombreEstadio, 
                self.ubicacion, self.capacidad)
    