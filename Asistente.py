class Asistente: 
    
    def __init__ (self, idEstadio , nombre, apellido, edad, DNI, plazaEstadio):
        self.idEstadio = idEstadio
        self.nombre = nombre
        self.apellido = apellido
        self.edad = edad
        self.DNI = DNI
        self.plazaEstadio = plazaEstadio

    def __str__(self):
        return ("\nid del estadio: {0} \nnombre: {1} \napellido: {2} \nedad: {3} \nDNI: {4} \nplaza Estadio: {5}"
                .format(self.idEstadio, self.nombre, self.apellido, self.edad, self.DNI, self.plazaEstadio))
    