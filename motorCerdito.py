import time
import network
from umqtt.simple import MQTTClient
from machine import Pin

# Configuración del broker MQTT
MQTT_BROKER = "broker.emqx.io"
MQTT_USER = ""
MQTT_PASSWORD = ""
MQTT_CLIENT_ID = "esp32_motor_client"
MQTT_TOPIC_PROXIMIDAD = "bldh/proximidad"
MQTT_PORT = 1883

# Definir los pines de control del motor
IN1 = Pin(27, Pin.OUT)
IN2 = Pin(14, Pin.OUT)
IN3 = Pin(12, Pin.OUT)
IN4 = Pin(13, Pin.OUT)

# Secuencia para el motor a pasos (estilo paso completo)
sec_anticlockwise = [
    [1, 0, 0, 1],
    [1, 0, 0, 0],
    [1, 1, 0, 0],
    [0, 1, 0, 0],
    [0, 1, 1, 0],
    [0, 0, 1, 0],
    [0, 0, 1, 1],
    [0, 0, 0, 1]
]

sec_clockwise = [
    [0, 0, 0, 1],
    [0, 0, 1, 1],
    [0, 1, 1, 0],
    [0, 1, 0, 0],
    [1, 1, 0, 0],
    [1, 0, 0, 0],
    [1, 0, 0, 1],
    [1, 0, 1, 0]
]

# Función para conectar a WiFi
def conectar_wifi():
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    sta_if.connect('UTNG_GUEST', 'R3d1nv1t4d0s#UT')  # Cambia esto por tu red WiFi
    while not sta_if.isconnected():
        time.sleep(0.3)
    print("WiFi Conectada!")

# Función para conectar al broker MQTT
def conectar_mqtt():
    client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER, port=MQTT_PORT, user=MQTT_USER, password=MQTT_PASSWORD)
    try:
        client.connect()
        print("Conectado al broker MQTT")
    except Exception as e:
        print(f"Error al conectar con MQTT: {e}")
        client = None
    return client

# Función para mover el motor en sentido horario
def mover_motor_clockwise(pasos, retardo=0.001):
    for _ in range(pasos):
        for secuencia in sec_clockwise:
            IN1.value(secuencia[0])
            IN2.value(secuencia[1])
            IN3.value(secuencia[2])
            IN4.value(secuencia[3])
            time.sleep(retardo)

# Función para mover el motor en sentido antihorario
def mover_motor_anticlockwise(pasos, retardo=0.001):
    for _ in range(pasos):
        for secuencia in sec_anticlockwise:
            IN1.value(secuencia[0])
            IN2.value(secuencia[1])
            IN3.value(secuencia[2])
            IN4.value(secuencia[3])
            time.sleep(retardo)

# Función para manejar los mensajes MQTT
def llegada_mensaje(topic, msg):
    print("Mensaje recibido:", msg)
    if topic == b"bldh/proximidad" and msg == b"proximo":
        # Activar el motor cuando se recibe el mensaje
        mover_motor_clockwise(200)  # Gira el motor en sentido horario
        time.sleep(1)
        mover_motor_anticlockwise(200)  # Gira el motor en sentido antihorario

# Función para suscribirse al broker MQTT
def subscribir():
    client = conectar_mqtt()
    client.set_callback(llegada_mensaje)
    client.subscribe(MQTT_TOPIC_PROXIMIDAD)
    print("Esperando mensajes en el tópico:", MQTT_TOPIC_PROXIMIDAD)
    return client

# Main loop
#def main():
#    conectar_wifi()
#    client = subscribir()

#    while True:
#        client.check_msg()  # Verificar si hay nuevos mensajes MQTT

#if name == 'main':
#main()
conectar_wifi()
client = subscribir()

while True:
    client.wait_msg()
