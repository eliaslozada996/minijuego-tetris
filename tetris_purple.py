import turtle
import random
import time
import pygame
pygame.mixer.init()





# ---------------- CONFIGURACIÓN ----------------
ANCHO, ALTO = 300, 600
TAM = 20
COLUMNAS = ANCHO // TAM
FILAS = ALTO // TAM

VELOCIDAD_BASE = 0.45
VELOCIDAD_MOV = 0.08

MAX_NIVELES = 5
TIEMPO_POR_NIVEL = 25

estado = "MENU"
modo = None

nivel = 1
velocidad_caida = VELOCIDAD_BASE
tiempo_inicio = 0

ultimo_tiempo = time.time()

puntaje = 0
tablero = [[0 for _ in range(COLUMNAS)] for _ in range(FILAS)]

pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.mixer.init()
pygame.mixer.music.set_volume(0.5)



# ---------------- PANTALLA ----------------
pantalla = turtle.Screen()
pantalla.setup(500, 650)
pantalla.bgcolor("#1c1c1c")
pantalla.title("Tetris - Turtle")
pantalla.tracer(0)

pygame.mixer.init()

def iniciar_musica():
    pygame.mixer.music.load("musica.wav")
    pygame.mixer.music.set_volume(0.4)
    pygame.mixer.music.play(-1)

def detener_musica():
    pygame.mixer.music.stop()



dib = turtle.Turtle()
dib.hideturtle()
dib.penup()
dib.speed(0)

def iniciar_musica():
    pygame.mixer.music.load("musica.mp3")
    pygame.mixer.music.set_volume(0.4)
    pygame.mixer.music.play(-1)

def detener_musica():
    pygame.mixer.music.stop()


# ---------------- PIEZAS ----------------
FORMAS = [
    [[1, 1, 1, 1]],
    [[1, 1], [1, 1]],
    [[0, 1, 0], [1, 1, 1]],
    [[1, 0, 0], [1, 1, 1]],
    [[0, 0, 1], [1, 1, 1]]
]

COLORES = ["cyan", "yellow", "purple", "blue", "orange"]

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
                        detener_musica()
                        return
                    tablero[self.pieza.y - y][self.pieza.x + x] = self.pieza.color
        limpiar_lineas()
        self.pieza = Pieza()
        if self.colision():
            estado = "GAME_OVER"
            detener_musica()

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


    # -------- CAÍDA DIRECTA (ESPACIO) --------
    def caer_directo(self):
        while not self.colision(dy=-1):
            self.pieza.y -= 1
        self.fijar()
        



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
    dib.color("gray30")
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
    dib.goto(0, 80)
    dib.write("BIENVENIDO A TETRIS", align="center", font=("Arial", 28, "bold"))
    dib.goto(0, 10)
    dib.write("1 - MODO ARCADE", align="center", font=("Arial", 16, "normal"))
    dib.goto(0, -30)
    dib.write("2 - JUGAR POR NIVELES", align="center", font=("Arial", 16, "normal"))
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
                dibujar_celda(juego.pieza.x + x, juego.pieza.y - y, juego.pieza.color)

    dib.goto(160, 250)
    dib.color("white")
    dib.write(f"Puntaje:\n{puntaje}", align="center", font=("Arial", 12, "bold"))

    if modo == "NIVEL":
        tiempo_restante = TIEMPO_POR_NIVEL - int(time.time() - tiempo_inicio)
        if tiempo_restante < 0:
            tiempo_restante = 0

        dib.goto(160, 210)
        dib.color("orange")
        dib.write(f"Nivel: {nivel}", align="center", font=("Arial", 12, "bold"))
        dib.goto(160, 180)
        dib.write(f"Tiempo: {tiempo_restante}s", align="center", font=("Arial", 12, "bold"))

    pantalla.update()

def dibujar_game_over():
    dib.clear()
    dib.color("red")
    dib.goto(0, 30)
    dib.write("PERDISTE 😂😂😂", align="center", font=("Arial", 18, "bold"))
    dib.goto(0, -20)
    dib.color("white")
    dib.write("Presiona ENTER para volver al menú", align="center", font=("Arial", 12, "normal"))
    pantalla.update()

# ---------------- CONTROLES ----------------
def iniciar_arcade():
    global estado, modo, tablero, puntaje
    if estado != "MENU":
        return
    tablero = [[0 for _ in range(COLUMNAS)] for _ in range(FILAS)]
    puntaje = 0
    modo = "ARCADE"
    estado = "JUGANDO"
    
def iniciar_arcade():
    global modo, estado
    modo = "ARCADE"
    estado = "JUGANDO"
    iniciar_musica()  


def iniciar_niveles():
    global modo, estado, nivel, velocidad_caida, tiempo_inicio
    modo = "NIVEL"
    nivel = 1
    velocidad_caida = VELOCIDAD_BASE
    tiempo_inicio = time.time()
    estado = "JUGANDO"
    iniciar_musica()   # 👈 AGREGA ESTA LÍNEA


def volver_menu():
    global estado, modo
    modo = None
    estado = "MENU"

def caer_rapido():
    if estado == "JUGANDO":
        juego.caer_directo()

pantalla.listen()
pantalla.onkeypress(iniciar_arcade, "1")
pantalla.onkeypress(iniciar_niveles, "2")
pantalla.onkeypress(volver_menu, "Return")

pantalla.onkeypress(lambda: juego.mover(-1), "Left")
pantalla.onkeypress(lambda: juego.mover(1), "Right")
pantalla.onkeypress(lambda: juego.bajar(), "Down")
pantalla.onkeypress(lambda: juego.rotar(), "Up")
pantalla.onkeypress(caer_rapido, "space")

# ---------------- LOOP ----------------
juego = Juego()

def loop():
    global ultimo_tiempo, tiempo_inicio, estado, nivel, velocidad_caida

    ahora = time.time()

    if estado == "MENU":
        dibujar_menu()

    elif estado == "JUGANDO":
        if ahora - ultimo_tiempo > velocidad_caida:
            juego.bajar()
            ultimo_tiempo = ahora

        if modo == "NIVEL":
            if ahora - tiempo_inicio >= TIEMPO_POR_NIVEL:
                if nivel < MAX_NIVELES:
                    nivel += 1
                    velocidad_caida *= 0.85
                    tiempo_inicio = time.time()
                else:
                    estado = "MENU"

        dibujar_juego()

    elif estado == "GAME_OVER":
        dibujar_game_over()

    pantalla.ontimer(loop, 16)

loop()
pantalla.mainloop()
