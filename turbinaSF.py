import time
import threading

class Turbina():
    def __init__(self) -> None:
        self.Valvula = 0.0
        self.junta = False
        self.Q1 = False
        self.Q2 = False
        self.QE = False
        self.motorAux = False
        self.freno = 0.0
        self.frenoEmergencia = False
        self.RPM = 0.0
        self.friccion = 20.0
        self.presionGas = 0.0
        self.temperatura = 0.0 
        self.aporteMotor = 0.0
        self.aporteQ = 0.0
        self.anteriores = []
        
    #Se intentan implementar hilos para correr un lazo PID de regulacion de temperatura y presion automatica en forma paralela sin éxito
    # A CORREGIR
        self.autoPID = threading.Event()

        self.hiloTemp = threading.Thread(
            target = self.PID,
            args = (self.temperatura, True, 0.0, 200.0),
            daemon=True
        )

        self.hiloPresion = threading.Thread(
            target = self.PID,
            args = (self.presionGas, True, 0.0, 4.5),
            daemon=True
        )

    def update(self):
        

        self.autoPID.set()
    # Si la junta neumática esta en True y el motor auxiliar esta encendido, el aporte de aceleración es 100, de lo contrario se restablece a cero. 
        if self.motorAux and self.junta:
            self.aporteMotor = 100.0
        else:
            self.aporteMotor = 0.0
    # Si ambos quemadores estan encendidos y la velocidad es mayor a 478, el aporte de aceleración sera proporcional a la apertura de la Válvula
    # Se agrega la variable glas acá de forma provisoria para implementar la secuencia del freno de emergencia
        if self.Q1 and self.Q2 and self.RPM > 478.0: 
            self.aporteQ = self.Valvula 
            self.presionGas += 0.09
        elif self.Q1 == 0 and self.Q2 == 0:
            self.aporteQ = 0.0
            self.presionGas -= 0.09
        
        if self.presionGas < 0.0:
            self.presionGas = 0.0

    # Ecuación para actualizar el aporte de aceleración y desaceleración de la turbina
        self.RPM += self.aporteMotor + self.aporteQ - self.friccion

    # La temperatura aumenta con el tiempo mientras la turbina este activa
        self.temperatura += 1.0
        
        
        if self.freno > 0.0:
            self.RPM -= self.freno

        self.RPM -= self.friccion

        if self.frenoEmergencia:
            self.Valvula = 0.0
            self.QE = True
            self.freno = 100.0
            
        if self.RPM <= 0.0:
            self.RPM = 0.0
    
    # desactivar esta sección si se logra hacer funcionar el lazo PID con la regulación de la temeperatura y la presion, por ahora se
    # agregan estas condicionales para evitar que se active el freno de emergencia por estas dos condiciones
        if self.presionGas >= 5.5:
            self.presionGas = 5.5
        if self.temperatura >= 350.0:
            self.temperatura = 350.0
        
    # Secuencia de frenado de emergencia
        if self.RPM > 5500.0 or self.presionGas > 5.5 or self.temperatura > 350.0:
            self.frenoEmergencia = True
            self.Valvula = 0.0

        if self.RPM > 4000.0:
            if self.presionGas < 3.3:
                time.sleep(3.0)
                self.frenoEmergencia = True
                self.Valvula = 0.0

    def PID(self,input, Man_Auto = False, SetpointMan = 0.0, SetpointAuto = 0.0):
            """
                Calcula la salida de un controlador PID (Proporcional, Integral, Derivativo).

                Args:
                    Man_Auto (bool): Modo manual (True) o automático (False).
                    SetpointMan (bool): Ignorado si Man_Auto es True. Modo manual de setpoint (True) o automático (False).
                    SetpointAuto (float): El valor del setpoint en modo automático.

                Returns:
                    None

                El método calcula la salida del controlador PID utilizando el valor actual (input) y el setpoint (SetpointAuto).
                Se almacena el histórico de velocidades en self.anteriores y se limita a 100 elementos.
                Se calculan los componentes P, I y D del controlador y se suman para obtener la salida.
                La salida se limita al rango de 0 a 100.

                """
            if Man_Auto == False:     
                # Si el PID está en modo automático...

                # Almaceno el vector velocidad en una lista de 100 elementos.
                self.anteriores.append(input)
                if len(self.anteriores) > 100:
                    self.anteriores = self.anteriores[-100:]

                SP = SetpointAuto        
                E = SP - input
                self.error = E 
                
                #error es la diferencia entre lo que tengo, y mi setpoint actual. Usamos la lista para ello. 
                E_accu = [(SP - elem) for elem in self.anteriores[-20:]]
                self.error_accu = E_accu
                
                kP = 2.0
                kI = 0.0001
                kD = 0.05

                #La acción proporcional es el error multiplicado por una constante
                aP = self.error * kP
                
                #La acción integral es el área de los valores, dividido por la constante
                aI = (kP * (sum(self.error_accu) / (len(self.error_accu)*0.002) * kI))

                #La acción derivativa es la proyección a futuro (pendiente) del error, multiplicado por una constante
                if len(self.anteriores)>2:
                    aD = (self.error_accu[-1]-self.error_accu[-2])*kD*kP
                else:
                    aD = 0.0
                
                #sumamos las componentes de las acciones Proporcional, Integral y Derivativa
                Salida = self.Valvula + aP + aI + aD

                #Limitamos la válvula de salida
                if Salida < 0:
                    self.Valvula = 0
                elif Salida > 100:
                    self.Valvula = 100         
                else:
                    self.Valvula = Salida

            else:
                # Si estamos en modo "Manual", la válvula se pone en la posición que definimos en el setpoint.
                self.Valvula = SetpointMan

TUR = Turbina()
estado = 1
TUR.update()
if TUR.autoPID.is_set():
    TUR.hiloTemp.start()
    TUR.hiloPresion.start()

try:
    while True:
        if estado == 1:
            TUR.junta = True
            #time.sleep(2.0)
            TUR.motorAux = True
            if TUR.RPM >= 478.0:
                estado += 1
        elif estado == 2:
            TUR.Q1 = True
            TUR.Q2 = True
            time.sleep(2.0)
            TUR.Valvula = 10.0
            if TUR.Q1 and TUR.Q2:
                estado += 1
        elif estado == 3:
            TUR.Valvula = 25.0
            if TUR.RPM > 2750.0:
                TUR.motorAux = False
                time.sleep(3.0)
                TUR.junta = False
                estado += 1
        elif estado == 4:
            TUR.PID(input=TUR.RPM, Man_Auto = False, SetpointAuto=4600.0)

        if estado == 5:
            TUR.PID(input=TUR.Valvula, Man_Auto = True, SetpointMan=10.0)
            time.sleep(0.2)
            TUR.Valvula = 0.0
            TUR.Q1 = False
            TUR.Q2 = False
            if TUR.RPM <=2500.0:
                TUR.freno = 100.0

        if TUR.freno == True:
            estado = "Frenado manual"

        if TUR.frenoEmergencia == True:
            estado = "Frenado de Emergencia"

        TUR.update()
        print(f"Presion: {TUR.presionGas:.2f}, Temp: {TUR.temperatura:.2f}")
        print(f"VEL: {TUR.RPM:.2f}, VALV: {TUR.Valvula:.2f}, Estado {estado}")
        #print(f"autoPID: {TUR.autoPID.is_set()}, hiloPresion: {TUR.hiloPresion.is_alive()}, hiloTemp: {TUR.hiloTemp.is_alive()}")
        time.sleep(0.1)
    
except KeyboardInterrupt:
    print("Simulación finalizada")
    TUR.autoPID.clear()
