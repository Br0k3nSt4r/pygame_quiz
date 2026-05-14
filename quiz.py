import pygame
import math
import random
import sys

# 1. Inicialización
pygame.init()

# 2. Configuración de pantalla
width, height = 600, 400
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Tren a toda velocidad - Versión Estable")

# 3. Colores
cielo = (75, 139, 225)
cesped = (43, 177, 57)
sol_color = (255, 255, 0)
montaña_color = (34, 139, 34)
blanco = (255, 255, 255)
negro = (0, 0, 0)
gris_claro = (180, 180, 180)
gris_oscuro = (100, 100, 100)
amarillo_cara = (255, 220, 100)

# 4. Variables de animación
reloj = pygame.time.Clock()
offset_railes = 0
humo_particulas = [] # Cada partícula será: [x, y, radio]
angulo_rueda = 0
train_x = 70 

# Variables para el fondo móvil
montañas_x = [20, 300, 550]
sol_x = 530

def dibujar_todo():
    global offset_railes, angulo_rueda, sol_x

    # --- FONDO ---
    screen.fill(cielo)
    
    # Sol
    sol_x += 0.2
    if sol_x > width + 50: sol_x = -50
    pygame.draw.circle(screen, sol_color, (int(sol_x), 80), 40)
    
    # Montañas
    for i in range(len(montañas_x)):
        x = montañas_x[i]
        pygame.draw.polygon(screen, montaña_color, [(x, 330), (x + 100, 150), (x + 200, 330)])
        montañas_x[i] += 3 
        if montañas_x[i] > width:
            montañas_x[i] = -200

    # Césped
    pygame.draw.rect(screen, cesped, (0, 330, 600, 70))

    # --- RAÍLES ---
    pygame.draw.line(screen, negro, (0, 360), (600, 360), 4)
    offset_railes = (offset_railes + 10) % 60
    for x in range(-100, 700, 60):
        pygame.draw.rect(screen, (100, 50, 0), (x + offset_railes, 360, 20, 10))

    # --- HUMO ---
    if random.random() > 0.92:
        humo_particulas.append([train_x + 145, 170, 6]) 

    for p in humo_particulas[:]:
        pygame.draw.circle(screen, (220, 220, 220), (int(p[0]), int(p[1])), int(p[2]))
        p[1] -= 2   # Sube
        p[0] += 3   # Se queda atrás
        p[2] += 0.2 # Crece
        if p[1] < 0: humo_particulas.remove(p)

    # --- EL TREN ---
    # Chimenea
    pygame.draw.rect(screen, gris_oscuro, (train_x + 120, 170, 50, 60))
    pygame.draw.rect(screen, negro, (train_x + 110, 160, 70, 15))
    
    # Cuerpo y Cabina
    pygame.draw.rect(screen, gris_claro, (train_x + 100, 230, 250, 90))
    pygame.draw.rect(screen, gris_oscuro, (train_x + 250, 150, 110, 100))
    pygame.draw.rect(screen, negro, (train_x + 240, 140, 130, 15))
    pygame.draw.rect(screen, blanco, (train_x + 270, 170, 70, 60))
    pygame.draw.ellipse(screen, gris_oscuro, (train_x + 60, 243, 40, 65))
    pygame.draw.rect(screen, gris_oscuro, (train_x + 70, 230, 20, 90))
    pygame.draw.rect(screen, negro, (train_x + 90, 241, 15, 70))

    # Cara
    pygame.draw.circle(screen, amarillo_cara, (train_x + 305, 200), 25)
    pygame.draw.circle(screen, negro, (train_x + 295, 195), 3)
    pygame.draw.circle(screen, negro, (train_x + 315, 195), 3)
    pygame.draw.circle(screen, (150, 0, 0), (train_x + 305, 215), 6)

    # Texto
    fuente = pygame.font.SysFont("Arial", 30, bold=True)
    txt = fuente.render("Diego", True, negro)
    screen.blit(txt, (train_x + 135, 255))

    # Ruedas y Bielas
    angulo_rueda -= 0.2
    ruedas_x = [train_x + 150, train_x + 230, train_x + 310]
    pos_bielas = []
    for rx in ruedas_x:
        pygame.draw.circle(screen, gris_oscuro, (rx, 320), 35)
        pygame.draw.circle(screen, negro, (rx, 320), 35, 3)
        bx = rx + int(math.cos(angulo_rueda) * 20)
        by = 320 + int(math.sin(angulo_rueda) * 20)
        pos_bielas.append((bx, by))

    pygame.draw.line(screen, negro, pos_bielas[0], pos_bielas[2], 8)

# 5. Bucle Principal
while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    dibujar_todo()
    pygame.display.flip()
    reloj.tick(30)