
class Tanque:
    nivelActual = 0.0
    caudal = 0.0
    volumenActual = 0.0
    
  
    def __init__(self, diametro: 1.0, altura: 1.0, valvulas = []):
        self.diametro = diametro
        self.altura = altura
        self.valvulas = valvulas

    def calcularNivel(self):
        pass
    def update(self,tiempo):
        pass
    def cargarTanque(self):
        pass
    def vaciarTanque(self):
        pass

class Valvula:
    caudalActual = 0.0

    def __init__(self, caudal: 1.0, tipo: str = 'E'):
        self.caudal = caudal
        self.tipo = tipo

    def abrirValvula(self):
        pass
    def cerrarValvula(self):
        pass