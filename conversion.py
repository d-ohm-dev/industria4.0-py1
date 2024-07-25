# Diccionario de factores de conversión de años terrestres a años en otros planetas
factores_conversion = {
    "Mercurio": 0.2408467,
    "Venus": 0.61519726,
    "Marte": 1.8808158,
    "Júpiter": 11.862615,
    "Saturno": 29.447498,
    "Urano": 84.016846,
    "Neptuno": 164.79132
}

# Solicitar la edad del usuario en años terrestres
edad_terrestre = int(input("Ingresa tu edad en años terrestres: "))

# Calcular la edad en otros planetas
edades_planetas = {}
for planeta, factor_conversion in factores_conversion.items():
    edad_planeta = round(edad_terrestre / factor_conversion, 2)
    edades_planetas[planeta] = edad_planeta

# Mostrar la edad en otros planetas
print("Tu edad en otros planetas:")
for planeta, edad in edades_planetas.items():
    print(f"{planeta}: {edad} años")