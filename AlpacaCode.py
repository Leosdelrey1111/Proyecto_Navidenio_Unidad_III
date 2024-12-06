from machine import Pin, PWM
from time import sleep

# Configuración de los LEDs
led_alpaca = Pin(25, Pin.OUT)
led_capibara = Pin(14, Pin.OUT)


# Contadores
contador1 = 0


# Ciclo principal
while True:
    # Bucle para el primer contador
    while contador1 < 10:
        contador1 += 1
        led_alpaca.value(1)
        led_capibara.value(1) # Regresa el servo a 90 grados
        sleep(1)
        led_alpaca.value(0)
        led_capibara.value(0)
        sleep(1)
    contador1 = 0  # Reinicia el contador1
