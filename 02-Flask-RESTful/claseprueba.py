""" item = "variable"

class Test():
    def __init__(self, nombre, apellido):
        self.nombre = nombre
        self.apellido = item
    
    def __repr__(self):
        return "Clase creada"

clases = Test("benji", "Mtz")

print(clases.nombre, clases.apellido)
print(clases) """

c = 0 # global variable

def add():
    #global permite modificar la variable
    global c
    c = c + 2 # increment by 2 
    print("Inside add():", c)

add()
print("In main:", c)