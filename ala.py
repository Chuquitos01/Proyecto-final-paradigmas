import pygame
import random
import math
import io
from pygame import mixer
import sys

# arrancamos Pygame
pygame.init()

# arrancamos la pantalla
pantalla = pygame.display.set_mode((1080, 675))

# titulo del juego
pygame.display.set_caption('Invasion Alienigena')

# iconito
icono = pygame.image.load('./recursos/nave.png')
pygame.display.set_icon(icono)

# el fondo de pantalla
fondo = pygame.image.load('./recursos/fondo.png')

# sonidito de fondo
mixer.music.load('./recursos/sonidofondo.mp3')
mixer.music.set_volume(0.3)
mixer.music.play(-1)

# la fuente
ruta_fuente = './recursos/FreeSansBold.ttf'
fuente = pygame.font.Font(ruta_fuente, 24)

# el protagonista
personaje = pygame.image.load('./recursos/prota.png')
posicion_x_personaje = 508
posicion_y_personaje = 611
velocidad_x_personaje = 0
velocidad_y_personaje = 0

def posicionar_personaje(x, y):
    pantalla.blit(personaje, (posicion_x_personaje, posicion_y_personaje))

# los invasores
enemigo = []
posicion_x_enemigo = []
posicion_y_enemigo = []
velocidad_x_enemigo = []
velocidad_y_enemigo = []
num_enemigos = 10

for e in range(num_enemigos):
    enemigo.append(pygame.image.load('./recursos/ufo.png'))
    posicion_x_enemigo.append(random.randint(0, 1016))
    posicion_y_enemigo.append(random.randint(30, 300))
    velocidad_x_enemigo.append(5)
    velocidad_y_enemigo.append(10)

def posicionar_enemigo(x, y, ene):
    pantalla.blit(enemigo[ene], (posicion_x_enemigo[ene], posicion_y_enemigo[ene]))

# la bala
bala = pygame.image.load('./recursos/bala.png')
bala_inicio_x = 0
bala_inicio_y = 0
bala_fin_x = 0
bala_fin_y = 10
bala_visible = False

def disparar(x, y):
    global bala_visible
    bala_visible = True
    pantalla.blit(bala, (x + 24, y - 16))

# el puntaje
puntaje = 0
posicion_x_puntaje = 10
posicion_y_puntaje = 10

def mostrar_puntaje(x, y):
    texto = fuente.render(f'Puntaje: {puntaje}', True, (255, 255, 255))
    pantalla.blit(texto, (x, y))

# las colisiones
def detectar_colision(x1, y1, x2, y2):
    distancia = math.sqrt(math.pow(x2 - x1, 2) + math.pow(y2 - y1, 2))
    if distancia < 35:
        return True
    else:
        return False

# el Game Over
texto_game_over = pygame.font.Font(ruta_fuente, 60)

def texto_final():
    texto_superficie = texto_game_over.render('GAME OVER', True, (255, 0, 0))
    texto_rectangulo = texto_superficie.get_rect()
    texto_rectangulo.center = (pantalla.get_width() // 2, pantalla.get_height() // 2)
    pantalla.blit(texto_superficie, texto_rectangulo)

# la ventana de Game Over
def fin_juego():
    global posicion_x_personaje, posicion_y_personaje, puntaje
    while True:
        pantalla.blit(fondo, (0, 0))
        texto_final()
        mostrar_puntaje(450, 450)

        # el boton Reintentar
        pygame.draw.rect(pantalla, (0, 255, 0), (300, 500, 200, 50))
        texto_reintentar = fuente.render('Reintentar', True, (255, 255, 255))
        pantalla.blit(texto_reintentar, (350, 510))

        # el boton Salir
        pygame.draw.rect(pantalla, (255, 0, 0), (600, 500, 200, 50))
        texto_salir = fuente.render('Salir', True, (255, 255, 255))
        pantalla.blit(texto_salir, (650, 510))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                # si clickean en "Reintentar"
                if 300 <= mx <= 500 and 500 <= my <= 550:
                    puntaje = 0
                    posicion_x_personaje = 508
                    posicion_y_personaje = 611
                    for e in range(num_enemigos):
                        posicion_x_enemigo[e] = random.randint(0, 1016)
                        posicion_y_enemigo[e] = random.randint(30, 300)
                    return True
                # si clickean en "Salir"
                elif 600 <= mx <= 800 and 500 <= my <= 550:
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

# mantenemos la pantalla
pantalla_activa = True
while pantalla_activa:
    # dibujamos el fondo de pantalla
    pantalla.blit(fondo, (0, 0))

    # manejamos eventos del usuario
    for event in pygame.event.get():
        # si el usuario cierra la ventana
        if event.type == pygame.QUIT:
            pantalla_activa = False

        # si el usuario presiona una tecla
        if event.type == pygame.KEYDOWN:
            # movimiento del personaje
            if event.key == pygame.K_LEFT:
                velocidad_x_personaje = -3
            elif event.key == pygame.K_RIGHT:
                velocidad_x_personaje = +3
            elif event.key == pygame.K_DOWN:
                velocidad_y_personaje = +2
            elif event.key == pygame.K_UP:
                velocidad_y_personaje = -2
            elif event.key == pygame.K_a:
                velocidad_x_personaje = -3
            elif event.key == pygame.K_d:
                velocidad_x_personaje = +3
            elif event.key == pygame.K_s:
                velocidad_y_personaje = +2
            elif event.key == pygame.K_w:
                velocidad_y_personaje = -2
            # disparar
            elif event.key == pygame.K_SPACE:
                sonido_bala = mixer.Sound('./recursos/rayo encogedor.mp3')
                vol_deseado_bala = 0.5
                sonido_bala.set_volume(vol_deseado_bala)
                sonido_bala.play()
                # si no hay una bala visible, disparar
                if not bala_visible:
                    bala_inicio_y = posicion_y_personaje
                    bala_inicio_x = posicion_x_personaje
                    disparar(bala_inicio_x, bala_inicio_y)

        # si el usuario suelta una tecla
        if event.type == pygame.KEYUP:
            # detener el movimiento del personaje
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_DOWN or event.key == pygame.K_UP or event.key == pygame.K_a or event.key == pygame.K_d or event.key == pygame.K_s or event.key == pygame.K_w:
                velocidad_x_personaje = 0
                velocidad_y_personaje = 0

    # actualizar la posición del personaje según su velocidad
    posicion_x_personaje += velocidad_x_personaje
    # ajustar la posición del personaje dentro de los límites de la pantalla
    if posicion_x_personaje <= -2:
        posicion_x_personaje = -2
    elif posicion_x_personaje >= 1019:
        posicion_x_personaje = 1019
    elif posicion_y_personaje >= 611:
        posicion_y_personaje = 611
    elif posicion_y_personaje <= 0:
        posicion_y_personaje = 0
    elif posicion_y_personaje <= 520:
        posicion_y_personaje = 520
    # actualizar la posición vertical del personaje según su velocidad
    posicion_y_personaje += velocidad_y_personaje

    # mostrar al personaje en su nueva posición
    posicionar_personaje(posicion_x_personaje, posicion_y_personaje)

    # iterar sobre los enemigos
    for e in range(num_enemigos):
        # si un enemigo llega al borde inferior de la pantalla, terminar el juego
        if posicion_y_enemigo[e] > 480:
            if fin_juego():
                break

        # mover al enemigo en la pantalla
        posicion_x_enemigo[e] += velocidad_x_enemigo[e]
        # si el enemigo alcanza el borde izquierdo o derecho, invertir su dirección
        if posicion_x_enemigo[e] <= 0:
            velocidad_x_enemigo[e] = 5
            posicion_y_enemigo[e] += velocidad_y_enemigo[e]
        elif posicion_x_enemigo[e] >= 1016:
            velocidad_x_enemigo[e] = -5
            posicion_y_enemigo[e] += velocidad_y_enemigo[e]
        # si el enemigo alcanza el borde inferior, reposicionarlo
        elif posicion_y_enemigo[e] >= 610:
            posicion_x_enemigo[e] = 5
        # actualizar la posición vertical del personaje según su velocidad
        posicion_y_personaje += velocidad_y_personaje

        # detectar colisiones entre el enemigo y la bala del personaje
        colision = detectar_colision(posicion_x_enemigo[e], posicion_y_enemigo[e], bala_inicio_x, bala_inicio_y)
        if colision:
            # reproducir el sonido de explosión
            explosion = mixer.Sound('./recursos/EXPLOSION.mp3')
            vol_deseado = 0.5
            explosion.set_volume(vol_deseado)
            explosion.play()
            # reposicionar la bala y el enemigo, incrementar el puntaje
            bala_inicio_y = posicion_y_personaje
            bala_visible = False
            puntaje += 1
            posicion_x_enemigo[e] = random.randint(0, 1016)
            posicion_y_enemigo[e] = random.randint(30, 300)

        # mostrar al enemigo en su nueva posición
        posicionar_enemigo(posicion_x_enemigo[e], posicion_y_enemigo[e], e)

    # reposicionar la bala si sale de la pantalla
    if bala_inicio_y <= 16:
        bala_inicio_y = posicion_y_personaje
        bala_visible = False
    # mostrar la bala si está en vuelo
    if bala_visible:
        disparar(bala_inicio_x, bala_inicio_y)
        bala_inicio_y -= bala_fin_y

    # mostrar al personaje
    posicionar_personaje(posicion_x_personaje, posicion_y_personaje)
    # mostrar el puntaje
    mostrar_puntaje(posicion_x_puntaje, posicion_y_puntaje)
    # actualizar la pantalla
    pygame.display.update()
