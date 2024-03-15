import pygame
import sys
import subprocess

# iniciar pygame
pygame.init()

# dimensiones de la pantalla del juego
ancho_pantalla = 1080
alto_pantalla = 675

# colores
blanco = (255, 255, 255)
negro = (0, 0, 0)
rojo = (255, 0, 0)

# fuente
fuente_grande = pygame.font.Font('./recursos/FreeSansBold.ttf', 72)
fuente_chica = pygame.font.Font('./recursos/FreeSansBold.ttf', 24)

# crear la pantalla
pantalla = pygame.display.set_mode((ancho_pantalla, alto_pantalla))
pygame.display.set_caption('Invasion Alienigena')

def objetos_texto(texto, fuente, color):
    superficie_texto = fuente.render(texto, True, color)
    return superficie_texto, superficie_texto.get_rect()

def mostrar_texto(texto, fuente, color, x, y):
    texto_superficie, texto_rect = objetos_texto(texto, fuente, color)
    texto_rect.center = (x, y)
    pantalla.blit(texto_superficie, texto_rect)

# loop del juego
def inicio_juego():
    inicio = True

    while inicio:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:
                    inicio = False
                    # ejecutar el archivo ala.py
                    subprocess.Popen(['python', 'ala.py'])
                elif evento.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        pantalla.fill(negro)
        # cargar imagen de fondo
        fondo_img = pygame.image.load('./recursos/fondo.png')
        pantalla.blit(fondo_img, (0, 0))
        
        mostrar_texto('Invasion Alienigena', fuente_grande, rojo, ancho_pantalla / 2, alto_pantalla / 2 - 100)
        mostrar_texto('Presiona ENTER para empezar', fuente_chica, blanco, ancho_pantalla / 2, alto_pantalla / 2 + 50)
        mostrar_texto('Presiona ESC para salir', fuente_chica, blanco, ancho_pantalla / 2, alto_pantalla / 2 + 100)

        pygame.display.update()

inicio_juego()
