import time

class Turbina():
    def __init__(self) -> None:
        self.Valvula = 0.0
        self.motorAux = False
        self.junta = False
        self.Q1 = False
        self.Q2 = False
        self.QE = False
        self.modoControl = False
        self.freno = False
        self.RPM = 0.0
        self.friccion = 20.0
        
        self.aporteMotor = 0.0
        self.aporteQuemadores = 0.0
        self.anteriores = []


    def update(self):
        if self.motorAux and self.junta:
            self.aporteMotor = 100.0
        else:
            self.aporteMotor = 0.0

        if self.Q1 and self.Q2 and self.RPM > 478.0: 
            self.aporteQuemadores = self.Valvula * 1.0

        self.RPM += self.aporteMotor + self.aporteQuemadores - self.friccion

        self.RPM -= self.friccion
        if self.RPM <= 0.0:
            self.RPM = 0.0

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
                kI = 0.00001
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



try:
    while True:
        TUR.junta = True
        time.sleep(1.0)
        TUR.motorAux = True
        TUR.update()
        print(f"VEL: {TUR.RPM:.2f}, VALV: {TUR.Valvula:.2f}, Estado {estado}")
        time.sleep(0.5)
        if TUR.RPM > 478.0 and TUR.RPM < 600.0:
            estado += 1
        if estado == 2:
            TUR.Q1 = True
            TUR.Q2 = True
            time.sleep(1.0)
            TUR.Valvula = 10.0
            TUR.update()
            print(f"VEL: {TUR.RPM:.2f}, VALV: {TUR.Valvula:.2f}, Estado {estado}")
            if TUR.Q1 and TUR.Q2:
                estado += 1
        elif estado == 3:
            TUR.Valvula = 25.0
            print(f"VEL: {TUR.RPM:.2f}, VALV: {TUR.Valvula:.2f}, Estado {estado}")
            TUR.update()
            if TUR.RPM > 2750.0:
                TUR.junta = False
                time.sleep(1.0)
                TUR.motorAux = False
                estado += 1
                print(f"Junta: {TUR.junta}, Motor: {TUR.motorAux}")
        elif estado == 4:
            TUR.modoControl = True
            TUR.PID(input=TUR.RPM, Man_Auto=False, SetpointAuto=4600.0)
            TUR.update()    
            print(f"VEL: {TUR.RPM:.2f}, VALV: {TUR.Valvula:.2f}, Estado {estado}")
            print(f"Junta: {TUR.junta}, Motor: {TUR.motorAux}")
            time.sleep(0.5)

        time.sleep(0.1)
    #Esta es la linea de codigo que setea el Lazo PID, aca usar un "if velocidad > 1750: el Man_Auto = False y SetpointAuto = 4600.0 RPMs"
        #TUR.PID(input=TUR.RPM, Man_Auto=False, SetpointAuto=3000.0)
        #TUR.update()

        #print(f"VEL: {TUR.RPM:.2f}, VALV: {TUR.Valvula:.2f}")
        #time.sleep(0.1)
except KeyboardInterrupt:
    print("Simulación finalizada")