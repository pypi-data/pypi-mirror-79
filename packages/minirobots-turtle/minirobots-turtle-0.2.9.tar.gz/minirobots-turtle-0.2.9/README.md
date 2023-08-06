# Python client for Minirobots Turtle Robot

## Install

```sh
$ pip install minirobots-turtle
```

### Run the Minirobots Shell

```sh
$ minirobots-shell [vi]
Te damos la bienvenida a la interfaz interactiva de Minirobots!
Desde aquí podrás programar tu tortuga en tiempo real 

Para ver la ayuda completa escribí

    help(Turtle)

Si querés ver sólo la ayuda de alguna función específica,
como por ejemplo 'forward', escribí

    help(Turtle.forward)

>>>
```

### Run the Jupyter Notebook Tutorial

```sh
$ minirobots-tutorial
```

### Run the Serial Monitor (robot connected to USB port required)

```sh
$ minirobots-serial-monitor /dev/ttyUSB0
Connected to: /dev/ttyUSB0
Press Ctrl+C to exit


   /'\_/`\  __          __             /\ \            /\ \__
  /\      \/\_\    ___ /\_\  _ __   ___\ \ \____    ___\ \ ,_\   ____
  \ \ \__\ \/\ \ /' _ `\/\ \/\`'__\/ __`\ \ '__`\  / __`\ \ \/  /',__\
   \ \ \_/\ \ \ \/\ \/\ \ \ \ \ \//\ \L\ \ \ \L\ \/\ \L\ \ \ \_/\__, `\
    \ \_\\ \_\ \_\ \_\ \_\ \_\ \_\\ \____/\ \_,__/\ \____/\ \__\/\____/
     \/_/ \/_/\/_/\/_/\/_/\/_/\/_/ \/___/  \/___/  \/___/  \/__/\/___/

[  init  ] Minirobots starting...
[  init  ] MAC Address: 2c:3a:e8:15:34:20
[  init  ] Connecting to WiFi using Casa-E...Connected!
[  init  ] IP Address: 192.168.1.112
[ turtle ] Connecting to minirobots.local...Error:
[ turtle ] Connecting to api.minirobots.com.ar...Connected!
[ turtle ] Current firmware version: 0.3.5
[ turtle ] No firmware update found at api.minirobots.com.ar
[ server ] Multicast DNS responder started for minirobots-153420.local
[ server ] Minirobots Turtle API started on port 80
```

### Use Examples

Making a square (Interactive Shell)

```python
>>> turtle = Turtle('01234f')
>>> for _ in range(4):
...   turtle.forward(10)
...   turtle.right(90)
...
```

Making a star function (Standalone program)

```python
from  minirobots import Turtle

turtle = Turtle('01234f')
turtle.auto_send(False)

def star(turtle, n, side):
    for _ in range(n):
        turtle.forward(side)
        turtle.right(360 / n)
        turtle.forward(side)
        turtle.left(720 / n)
    turtle.send()

star(turtle, 5, 100)
```

### Primitives

Class Turtle

    class Turtle(code, ip=None)
        debug(on=None)
        auto_send(on=None)
        info()
        status()
        forward(distance)
        backward(distance)
        right(angle)
        left(angle)
        pen_up()
        pen_down()
        leds(red, green, blue, led=None)
        leds_color(color, led=None)
        random_leds(led=None)
        random_led_right()
        random_led_left()
        turn_off_leds(led=None)
        play_tone(frequency, duration=1000)
        play_note(note, duration=1000)
        play_random_note(duration=1000)
        sleep(duration=1000)
        queue_lock()
        queue_unlock()
        queue_clear()
        send(commands=None)
        stop()

        # Static methods
        get_random_color()
        get_random_note()
        get_frequency(note)

        # Properties
        ip
        ip_age

        # Constants
        LED_LEFT
        LED_RIGHT
        LED_BOTH
        COLORS
        NOTES

        # Aliases
        silence == sleep

Class Tortuga

    class Tortuga(code=None, ip=None)
        adelante(distancia)
        atras(distancia)
        derecha(angulo)
        izquierda(angulo)
        lapiz_arriba()
        lapiz_abajo()
        leds(rojo, verde, azul, led=None)
        leds_color(color, led=None)
        leds_al_azar(led=None)
        led_izquierdo_al_azar()
        led_derecho_al_azar()
        apagar_leds(led=None)
        tono(frecuencia, duracion=1000)
        nota(nota, duracion=1000)
        nota_al_azar(duracion=1000)
        esperar(duracion=1000)
        auto_enviar(activado=None)
        enviar()
        parar()

        # Aliases
        avanzar = adelante
        retroceder = atras
        subir_lapiz = lapiz_arriba
        bajar_lapiz = lapiz_abajo
        encender_leds = leds
        encender_leds_color = leds_color
        encender_leds_al_azar = leds_al_azar
        encender_led_derecho_al_azar = led_derecho_al_azar
        encender_led_izquierdo_al_azar = led_izquierdo_al_azar
        reproducir_tono = tono
        tocar_nota = nota
        tocar_nota_al_azar = nota_al_azar
        silencio = esperar
        obtener_color_al_azar = Turtle.get_random_color 
        obtener_nota_al_azar = Turtle.get_random_note

## Development

### Create environment

Use the bash script

```sh
$ bin/create_env.sh
```

Or create it manually

```sh
python3 -m venv env
source env/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```
