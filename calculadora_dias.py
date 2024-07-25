from datetime import date

# Obtener la fecha de nacimiento del usuario
anio_nacimiento = int(input("Ingresa el año de tu nacimiento (YYYY): "))
mes_nacimiento = int(input("Ingresa el mes de tu nacimiento (MM): "))
dia_nacimiento = int(input("Ingresa el día de tu nacimiento (DD): "))

# Obtener la fecha actual
fecha_actual = date.today()

# Crear el objeto de fecha de nacimiento
fecha_nacimiento = date(anio_nacimiento, mes_nacimiento, dia_nacimiento)

# Calcular la diferencia de días entre las fechas
diferencia = fecha_actual - fecha_nacimiento

# Mostrar el resultado
print("Has vivido", diferencia.days, "días.")