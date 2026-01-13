# minijuego-tetris

import turtle
import random
import time

# ---------------- CONFIGURACIÓN ----------------
ANCHO, ALTO = 300, 600
TAM = 20
COLUMNAS = ANCHO // TAM
FILAS = ALTO // TAM

VELOCIDAD_CAIDA = 0.12  # más rápido que antes
VELOCIDAD_MOV = 0.03    # movimiento lateral más ágil

estado = "MENU"  # empieza en menú
ultimo_tiempo = time.time()
ultimo_mov = time.time()

mov_izq = False
mov_der = False

puntaje = 0

tablero = [[0 for _ in range(COLUMNAS)] for _ in range(FILAS)]

pantalla = turtle.Screen()
pantalla.setup(500, 650)
pantalla.bgcolor("#1c1c1c")  # fondo gris oscuro
pantalla.title("Tetris - Turtle")
pantalla.tracer(0)

dib = turtle.Turtle()
dib.hideturtle()
dib.penup()
dib.speed(0)

# ---------------- PIEZAS ----------------
FORMAS = [
    [[1, 1, 1, 1]],           # I
    [[1, 1], [1, 1]],         # O
    [[0, 1, 0], [1, 1, 1]]    # T
]

COLORES = ["cyan", "yellow", "purple"]

class Pieza:
    def __init__(self):
        self.forma = random.choice(FORMAS)
        self.color = random.choice(COLORES)
        self.x = COLUMNAS // 2 - 1
        self.y = FILAS - 1

    def rotar(self):
        self.forma = [list(f) for f in zip(*self.forma[::-1])]

class Juego:
    def __init__(self):
        self.pieza = Pieza()

    def colision(self, dx=0, dy=0):
        for y, fila in enumerate(self.pieza.forma):
            for x, celda in enumerate(fila):
                if celda:
                    nx = self.pieza.x + x + dx
                    ny = self.pieza.y - y + dy
                    if nx < 0 or nx >= COLUMNAS or ny < 0:
                        return True
                    if ny < FILAS and tablero[ny][nx]:
                        return True
        return False

    def fijar(self):
        global estado
        for y, fila in enumerate(self.pieza.forma):
            for x, celda in enumerate(fila):
                if celda:
                    if self.pieza.y - y >= FILAS - 1:
                        estado = "GAME_OVER"
                        return
                    tablero[self.pieza.y - y][self.pieza.x + x] = self.pieza.color
        limpiar_lineas()
        self.pieza = Pieza()
        if self.colision():
            estado = "GAME_OVER"

    def bajar(self):
        if not self.colision(dy=-1):
            self.pieza.y -= 1
        else:
            self.fijar()

    def mover(self, dx):
        if not self.colision(dx=dx):
            self.pieza.x += dx

    def rotar(self):
        copia = self.pieza.forma
        self.pieza.rotar()
        if self.colision():
            self.pieza.forma = copia

# ---------------- LÓGICA ----------------
def limpiar_lineas():
    global tablero, puntaje
    nuevas = []
    eliminadas = 0

    for fila in tablero:
        if all(fila):
            eliminadas += 1
        else:
            nuevas.append(fila)

    for _ in range(eliminadas):
        nuevas.append([0] * COLUMNAS)

    tablero = nuevas
    puntaje += eliminadas * 100

# ---------------- DIBUJO ----------------
def dibujar_celda(x, y, color):
    dib.goto(x * TAM - ANCHO // 2, y * TAM - ALTO // 2)
    dib.color(color)
    dib.begin_fill()
    for _ in range(4):
        dib.forward(TAM)
        dib.left(90)
    dib.end_fill()

def dibujar_cuadricula():
    dib.color("gray20")
    for x in range(COLUMNAS + 1):
        dib.goto(x * TAM - ANCHO // 2, -ALTO // 2)
        dib.pendown()
        dib.goto(x * TAM - ANCHO // 2, ALTO // 2)
        dib.penup()
    for y in range(FILAS + 1):
        dib.goto(-ANCHO // 2, y * TAM - ALTO // 2)
        dib.pendown()
        dib.goto(ANCHO // 2, y * TAM - ALTO // 2)
        dib.penup()

def dibujar_menu():
    dib.clear()
    dib.color("white")
    dib.goto(0, 50)
    dib.write("TETRIS", align="center", font=("Arial", 32, "bold"))
    dib.goto(0, -20)
    dib.write("PRESS ENTER TO PLAY", align="center", font=("Arial", 16, "normal"))
    pantalla.update()

def dibujar_juego():
    dib.clear()
    dibujar_cuadricula()

    for y in range(FILAS):
        for x in range(COLUMNAS):
            if tablero[y][x]:
                dibujar_celda(x, y, tablero[y][x])

    for y, fila in enumerate(juego.pieza.forma):
        for x, celda in enumerate(fila):
            if celda:
                dibujar_celda(
                    juego.pieza.x + x,
                    juego.pieza.y - y,
                    juego.pieza.color
                )

    dib.goto(160, 250)
    dib.color("white")
    dib.write(f"Puntaje:\n{puntaje}", align="center", font=("Arial", 14, "bold"))
    pantalla.update()

def dibujar_game_over():
    dib.clear()
    dib.color("red")
    dib.goto(0, 50)
    dib.write("GAME OVER", align="center", font=("Arial", 32, "bold"))

    dib.goto(0, -20)
    dib.color("white")
    dib.write(f"Puntaje final: {puntaje}", align="center", font=("Arial", 16, "normal"))

    dib.goto(0, -60)
    dib.write("Presiona ESPACIO", align="center", font=("Arial", 12, "normal"))
    dib.goto(0, -80)
    dib.write("si desea reiniciar", align="center", font=("Arial", 12, "normal"))
    pantalla.update()

# ---------------- CONTROLES ----------------
def presionar_izq():
    global mov_izq
    if estado == "JUGANDO":
        mov_izq = True

def soltar_izq():
    global mov_izq
    mov_izq = False

def presionar_der():
    global mov_der
    if estado == "JUGANDO":
        mov_der = True

def soltar_der():
    global mov_der
    mov_der = False

def bajar():
    if estado == "JUGANDO":
        juego.bajar()

def rotar():
    if estado == "JUGANDO":
        juego.rotar()

def reiniciar():
    global tablero, puntaje, estado, juego
    tablero = [[0 for _ in range(COLUMNAS)] for _ in range(FILAS)]
    puntaje = 0
    juego = Juego()
    estado = "JUGANDO"

def iniciar_juego():
    global estado
    estado = "JUGANDO"

pantalla.listen()
pantalla.onkeypress(presionar_izq, "Left")
pantalla.onkeyrelease(soltar_izq, "Left")
pantalla.onkeypress(presionar_der, "Right")
pantalla.onkeyrelease(soltar_der, "Right")
pantalla.onkey(bajar, "Down")
pantalla.onkey(rotar, "Up")
pantalla.onkey(reiniciar, "space")
pantalla.onkey(iniciar_juego, "Return")  # ENTER inicia el juego

# ---------------- LOOP ----------------
juego = Juego()

def loop():
    global ultimo_tiempo, ultimo_mov

    ahora = time.time()

    if estado == "MENU":
        dibujar_menu()
    elif estado == "JUGANDO":
        if ahora - ultimo_tiempo > VELOCIDAD_CAIDA:
            juego.bajar()
            ultimo_tiempo = ahora

        if ahora - ultimo_mov > VELOCIDAD_MOV:
            if mov_izq:
                juego.mover(-1)
            if mov_der:
                juego.mover(1)
            ultimo_mov = ahora

        dibujar_juego()
    elif estado == "GAME_OVER":
        dibujar_game_over()

    pantalla.ontimer(loop, 16)

loop()
pantalla.mainloop()
