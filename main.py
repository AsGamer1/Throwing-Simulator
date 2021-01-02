# Imports
import pygame
import math
import random

# Pantalla e inicialización
Alto = 600
Ancho = 800
pygame.init()
fuente1 = pygame.font.Font(None, 20)
fuente2 = pygame.font.Font(None, 40)
screen = pygame.display.set_mode((Ancho, Alto))
pygame.display.set_caption("Throwing Simulator")
icon = pygame.image.load("icon.png")
background = pygame.image.load("background.png")
pygame.display.set_icon(icon)
clock = pygame.time.Clock()
menudisplay = True
running = True
siguiente = False
score_value = 0

# Classes


class Cursor(pygame.Rect):
    def __init__(self):
        pygame.Rect.__init__(self, 0, 0, 1, 1)

    def update(self):
        self.left, self.top = pygame.mouse.get_pos()


class Boton(pygame.sprite.Sprite):
    def __init__(self, imagen1, imagen2, x, y):
        self.imagen_normal = imagen1
        self.imagen_select = imagen2
        self.imagen_actual = self.imagen_normal
        self.rect = self.imagen_actual.get_rect()
        self.rect.left, self.rect.top = (x, y)

    def update(self, pantalla, cursors):
        if cursors.colliderect(self.rect):
            self.imagen_actual = self.imagen_select
        else:
            self.imagen_actual = self.imagen_normal
        pantalla.blit(self.imagen_actual, self.rect)


class Proyectil(pygame.sprite.Sprite):
    def __init__(self, x, y):
        self.image = pygame.image.load("roca.png")
        self.angulo = random.randint(0, 90)
        self.veloc = random.randint(10, 100)
        self.velocx = self.veloc * math.cos(math.radians(self.angulo))
        self.velocy = self.veloc * math.sin(math.radians(self.angulo))
        self.tiempo = 0
        self.x = x
        self.y = y
        self.disparar = False
        self.xreal = x
        self.yreal = Alto - self.y
        self.tiemporeal = 0
        self.ymax = Alto - self.y
        self.velocyreal = self.velocy + (-9.8 * self.tiempo)

    def update(self, pantalla):
        self.velocx = self.veloc * math.cos(math.radians(self.angulo))
        self.velocy = self.veloc * math.sin(math.radians(self.angulo))
        self.velocyreal = self.velocy + (-9.8 * self.tiempo)
        if self.disparar is True:
            self.xreal = (0 + self.velocx * self.tiempo)
            self.yreal = (0 + self.velocy * self.tiempo + (-9.8 * (self.tiempo ** 2)) / 2)
            self.x = self.xreal
            self.y = Alto - self.yreal
            self.tiemporeal = self.tiempo
            if self.velocyreal > 0:
                self.ymax = (0 + self.velocy * self.tiempo + (-9.8 * (self.tiempo ** 2)) / 2)
            else:
                pass

        else:
            pass
        if (self.y > Alto) or (self.x > (Ancho-64)):
            self.x = 0
            self.y = Alto
            self.tiempo = 0
            self.disparar = False

        if siguiente is True:
            self.x = 0
            self.y = Alto
            self.angulo = random.randint(0, 90)
            self.veloc = random.randint(10, 100)
            self.tiempo = 0
            self.disparar = False
        pantalla.blit(self.image, (self.x, (self.y-64)))


class Trayectoria(pygame.sprite.Sprite):
    def __init__(self, x, angulo, veloc, pantalla):
        self.image = pygame.image.load("trayectoria.png")
        self.x = x
        self.angulo = angulo
        self.veloc = veloc
        self.y = ((-9.8/(2*(self.veloc**2)*(math.cos(math.radians(self.angulo)))**2))*(x**2) +
                  (math.tan(math.radians(self.angulo)))*x)
        self.yreal = Alto - self.y
        pantalla.blit(self.image, ((self.x+24), (self.yreal-40)))


class Objetivo(pygame.sprite.Sprite):
    def __init__(self, imagen):
        self.image = pygame.image.load(imagen)
        self.x = random.randint(150, 544)
        self.y = Alto - 192

    def update(self, pantalla):
        pantalla.blit(self.image, (self.x, (self.y-64)))


# Cursor
cursor = Cursor()

# Carga de imágenes
ajustes = pygame.image.load("ajustes.png")
ajustes_select = pygame.image.load("ajustes_select.png")
play = pygame.image.load("play.png")
play_select = pygame.image.load("play_select.png")
abajo = pygame.image.load("abajo.png")
abajopres = pygame.image.load("abajopres.png")
arriba = pygame.image.load("arriba.png")
arribapres = pygame.image.load("arribapres.png")

# Botones
botonajustes = Boton(ajustes, ajustes_select, 70, 10)
botonplay = Boton(play, play_select, 30, 10)
botonabajoang = Boton(abajo, abajopres, 297, 30)
botonabajovel = Boton(abajo, abajopres, 183, 30)
botonarribaang = Boton(arriba, arribapres, 312, 30)
botonarribavel = Boton(arriba, arribapres, 198, 30)


# Proyectil y objetivos
bala = Proyectil(0, Alto)
castillo1 = Objetivo("castillo1.png")
castillo2 = Objetivo("castillo2.png")
castillo3 = Objetivo("castillo3.png")
castillo4 = Objetivo("castillo4.png")
castillo5 = Objetivo("castillo5.png")
castillo6 = Objetivo("castillo6.png")
listacastillos = [castillo1, castillo2, castillo3, castillo4, castillo5, castillo6]
random.shuffle(listacastillos)
castillo = listacastillos[0]


# Main loop
while running:
    tick = clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            if cursor.colliderect(botonplay.rect):
                bala.disparar = True
            elif cursor.colliderect(botonajustes.rect):
                if menudisplay is True:
                    menudisplay = False
                elif menudisplay is False:
                    menudisplay = True
            elif cursor.colliderect(botonabajoang.rect):
                if bala.angulo > 0 and bala.disparar is False:
                    bala.angulo = bala.angulo - 1
            elif cursor.colliderect(botonarribaang.rect):
                if bala.angulo < 90 and bala.disparar is False:
                    bala.angulo = bala.angulo + 1
            elif cursor.colliderect(botonabajovel.rect):
                if bala.veloc > 10 and bala.disparar is False:
                    bala.veloc = bala.veloc - 1
            elif cursor.colliderect(botonarribavel.rect):
                if bala.veloc < 100 and bala.disparar is False:
                    bala.veloc = bala.veloc + 1
        elif event.type == pygame.QUIT:
            running = False
    if bala.disparar is True:
        bala.tiempo = bala.tiempo + (tick/1000.0)

# Textos
    text1 = "Velocidad: %d (m/s)   Angulo: %d   x= %d m   y= %d m   t= %.2f s   y(max)= %d m" % (
        bala.veloc, bala.angulo, bala.xreal, bala.yreal, bala.tiemporeal, bala.ymax)
    mensaje1 = fuente1.render(text1, True, (0, 0, 0))

    text2 = "Puntuación: %d puntos" % score_value
    mensaje2 = fuente2.render(text2, True, (255, 255, 255))

# Fondos
    screen.blit(background, (0, 50))
    pygame.draw.rect(screen, (191, 191, 191), (0, 0, 800, 50))
    pygame.draw.line(screen, (0, 0, 0), (0, 50), (800, 50), 2)
    if menudisplay:
        pygame.draw.rect(screen, (255, 255, 255), (110, 0, 690, 50))
        botonabajoang.update(screen, cursor)
        botonabajovel.update(screen, cursor)
        botonarribaang.update(screen, cursor)
        botonarribavel.update(screen, cursor)
        screen.blit(mensaje1, (120, 20))
    elif not menudisplay:
        pygame.draw.rect(screen, (191, 191, 191), (110, 0, 690, 50))
    screen.blit(mensaje2, (450, 70))


# Botones
    cursor.update()
    botonplay.update(screen, cursor)
    botonajustes.update(screen, cursor)

# Bala
    bala.update(screen)
    rectangulobala = bala.image.get_rect()
    rectangulobala.left, rectangulobala.top = (bala.x, (bala.y - 64))

# Castillos
    castillo.update(screen)
    rectangulocastillo = castillo.image.get_rect()
    rectangulocastillo.left, rectangulocastillo.top = (castillo.x+40, (castillo.y+10))
    rectangulocastillo.height, rectangulocastillo.width = (
        rectangulocastillo.height - 80, rectangulocastillo.width - 80)

# Trayectoria
    distancia = castillo.x - bala.x
    if bala.disparar is False:
        punto0 = Trayectoria(32, bala.angulo, bala.veloc, screen)
        punto1 = Trayectoria((distancia / (4 / 3)), bala.angulo, bala.veloc, screen)
        punto2 = Trayectoria((distancia / 2), bala.angulo, bala.veloc, screen)
        punto3 = Trayectoria((distancia / 4), bala.angulo, bala.veloc, screen)
    else:
        pass

# Colisión
    if rectangulocastillo.colliderect(rectangulobala):
        castillo.x = random.randint(150, 544)
        random.shuffle(listacastillos)
        castillo = listacastillos[0]
        score_value += 1
        siguiente = True
    else:
        siguiente = False

    pygame.display.update()
