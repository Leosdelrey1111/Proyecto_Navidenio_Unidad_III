import network
from umqtt.simple import MQTTClient
from machine import Pin, PWM
import neopixel
from time import sleep
import time
import _thread

# Configuración del broker MQTT
MQTT_BROKER = "broker.emqx.io"
MQTT_USER = ""
MQTT_PASSWORD = ""
MQTT_CLIENT_ID = "esp32_client"
MQTT_TOPIC_PROXIMIDAD = "bldh/proximidad"
MQTT_COMMAND_TOPIC = "bldh/comando"
MQTT_PORT = 1883

# Configuración para la tira LED
NUM_LEDS = 60
PIN_LEDS = 23
led_strip = neopixel.NeoPixel(Pin(PIN_LEDS), NUM_LEDS)

# Configuración del buzzer
buzzer = Pin(27, Pin.OUT)
buzzer_pwm = PWM(buzzer, freq=1, duty=0)  # PWM para el buzzer

# Configuración del LED adicional en el pin 22
led_pin_22 = Pin(22, Pin.OUT)

# Definir las notas musicales
NOTES = {
    'C': 261,
    'D': 294,
    'E': 329,
    'F': 349,
    'G': 392,
    'A': 440,
    'B': 466,
    'C5': 523,
}

# Canciones navideñas (frecuencias de notas)
JINGLE_BELLS = [
    'E', 'E', 'E', 'E', 'E', 'E', 'E', 'G', 'C5', 'B', 'A', 'A', 'A', 'B', 'B',
    'A', 'A', 'A', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'G', 'C5', 'B', 'A'
]

SILENT_NIGHT = [
    'E', 'D', 'C', 'D', 'E', 'E', 'E', 'D', 'D', 'D', 'E', 'C', 'E', 'C',
    'D', 'C', 'E', 'C', 'B', 'C', 'B', 'E', 'E', 'E',
    'E', 'D', 'C', 'D', 'E', 'E', 'E', 'D', 'D', 'D', 'E', 'C', 'E', 'C',
    'D', 'C', 'E', 'C', 'B', 'C', 'B', 'E', 'E', 'E'
]

# Función para conectar a WiFi
def conectar_wifi():
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    sta_if.connect('UTNG_GUEST', 'R3d1nv1t4d0s#UT')  # Cambia esto por tu red WiFi
    while not sta_if.isconnected():
        sleep(0.3)
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

# Variable global para controlar la canción en reproducción
cancion_reproduciendose = False
cancion_detener = False

# Función para reproducir una canción
def reproducir_cancion(cancion):
    global cancion_reproduciendose, cancion_detener

    if cancion_reproduciendose:
        print("Canción en reproducción. Deteniendo...")
        cancion_detener = True  # Señal para detener la canción actual

        # Esperar a que la canción se detenga
        while cancion_reproduciendose:
            sleep(0.1)

    cancion_reproduciendose = True  # Marca que la canción está en reproducción
    cancion_detener = False  # Reseteamos la bandera de detener

    for nota in cancion:
        if cancion_detener:  # Si se recibe la señal de detener, salimos del bucle
            break
        buzzer_pwm.freq(NOTES[nota])
        buzzer_pwm.duty(52)  # Sonido del buzzer
        sleep(0.3)  # Duración de la nota
        buzzer_pwm.duty(0)  # Silencio
        sleep(0.1)  # Tiempo entre notas

    cancion_reproduciendose = False  # Marca que la canción terminó

# Función para manejar los comandos de canciones a través de MQTT
def sub_cb(topic, msg):
    print(f"Comando recibido en {topic}: {msg}")
    if msg == b"jingle_bells":
        _thread.start_new_thread(reproducir_cancion, (JINGLE_BELLS,))  # Reproduce "Jingle Bells" en un hilo
    elif msg == b"silent_night":
        _thread.start_new_thread(reproducir_cancion, (SILENT_NIGHT,))  # Reproduce "Silent Night" en un hilo
    else:
        print("Comando no reconocido.")

# Función para conectar al broker MQTT y suscribirse al tema de comandos
def run_mqtt():
    client = conectar_mqtt()
    if client is None:
        print("Fallo al conectar al broker MQTT.")
        return

    client.set_callback(sub_cb)  # Establece el callback para manejar mensajes
    client.subscribe(MQTT_COMMAND_TOPIC)  # Se suscribe al tópico de comandos de canción
    print(f"Conectado al broker MQTT y suscrito a {MQTT_COMMAND_TOPIC}")

    while True:
        try:
            client.check_msg()  # Revisa los mensajes MQTT
        except OSError as e:
            print(f"Error en la comunicación MQTT: {e}. Intentando reconectar...")
            client = conectar_mqtt()  # Reconectar si se pierde la conexión
            if client is None:
                print("No se pudo reconectar al broker MQTT.")
                break  # Si no podemos reconectar, terminamos el bucle
        sleep(1)

def verificar_conexion(client):
    try:
        client.ping()  # Intentamos hacer un ping al broker
        return True
    except:
        print("Conexión perdida. Intentando reconectar...")
        return False

# Función para manejar el comportamiento de las luces según proximidad
def enviar_mensaje(client):
    global proximidad_activa, proximidad_contador

    try:
        if not verificar_conexion(client):
            client = conectar_mqtt()  # Intentamos reconectar si no hay conexión

        print("Enviando mensaje de proximidad...")
        client.publish(MQTT_TOPIC_PROXIMIDAD, b"proximo")  # Envía el mensaje al tópico de proximidad

        proximidad_activa = True  # Activamos la proximidad
        proximidad_contador = 0  # Reiniciamos el contador

        # Enciende el buzzer
        buzzer_pwm.freq(NOTES['E'])
        buzzer_pwm.duty(512)
        sleep(0.3)
        buzzer_pwm.duty(0)

        # Enciende el LED adicional en el pin 22
        led_pin_22.value(1)

        # Efecto de luces navideñas en la tira LED (colores secuenciales)
        for i in range(NUM_LEDS):
            color = (255, 0, 0) if i % 3 == 0 else (0, 255, 0) if i % 3 == 1 else (0, 0, 255)
            led_strip[i] = color
        led_strip.write()
        sleep(0.3)

        for i in range(NUM_LEDS):
            color = (255, 255, 255) if i % 3 == 0 else (0, 0, 0) if i % 3 == 1 else (255, 255, 0)
            led_strip[i] = color
        led_strip.write()
        sleep(0.3)

    except Exception as e:
        print(f"Error al publicar mensaje MQTT o manejar luces: {e}")
        # Intentar reconectar si ocurre algún error
        client = conectar_mqtt()
        if client is None:
            print("No se pudo reconectar al broker MQTT.")
            return
        else:
            print("Reconexión exitosa.")
            # Intentar publicar de nuevo
            try:
                client.publish(MQTT_TOPIC_PROXIMIDAD, b"proximo")  # Intentar publicar de nuevo
                print("Mensaje publicado correctamente tras reconexión.")
            except Exception as reconnection_error:
                print(f"Error al publicar después de reconectar: {reconnection_error}")

# Programa principal
def main():
    global proximidad_activa, proximidad_contador
    proximidad_activa = False
    proximidad_contador = 0

    conectar_wifi()
    client = conectar_mqtt()

    # Ejecutar el MQTT en un hilo
    _thread.start_new_thread(run_mqtt, ())

    try:
        while True:
            # Esperar 10 segundos antes de enviar el mensaje de proximidad
            sleep(10)
            enviar_mensaje(client)  # Enviar el mensaje de proximidad

    except KeyboardInterrupt:
        print("Programa terminado")
        buzzer_pwm.duty(0)  # Apaga el buzzer al finalizar
        led_pin_22.value(0)  # Apaga el LED en el pin 22
        for i in range(NUM_LEDS):
            led_strip[i] = (0, 0, 0)  # Apaga las luces al finalizar
        led_strip.write()
        client.disconnect()

if _name_ == '_main_':
    main()
