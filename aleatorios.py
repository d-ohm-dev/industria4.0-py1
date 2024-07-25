import numpy as np
import matplotlib.pyplot as plt

# Generar un array con 100 datos aleatorios
datos_aleatorios = np.random.rand(100)

# Crear una lista de índices para el eje x
indices = np.arange(100)

# Graficar los datos
plt.plot(indices, datos_aleatorios)
plt.xlabel('Índice')
plt.ylabel('Valor')
plt.title('Datos Aleatorios')
plt.show()