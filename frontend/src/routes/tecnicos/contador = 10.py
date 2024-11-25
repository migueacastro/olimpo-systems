import time

horas = int(input("Introduzca las horas"))
minutos = int(input("Introduzca los minutos"))
segundos = int(input("Introduzca los segundos"))

tiempo = (horas * 60 * 60) + (minutos * 60) + segundos

while tiempo > 0:
    horas_cronometro = tiempo // (60 * 60)
    minutos_cronometro = (tiempo // 60) - horas_cronometro * 60
    segundos_cronometro = (tiempo) - (minutos_cronometro * 60) - (horas_cronometro * 3600)
    print(f'{horas_cronometro}:{minutos_cronometro}:{segundos_cronometro}')
    time.sleep(1)
    tiempo -= 1