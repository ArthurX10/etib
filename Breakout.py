import random
import sys
import pygame

pygame.init()

# Configurações da tela
LARGURA, ALTURA = 600, 650
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Breakout Pygame")
relogio = pygame.time.Clock()

# Cores
FUNDO = (18, 20, 28)
BRANCO = (245, 245, 245)
AZUL_RAQUETE = (50, 170, 255)
AMARELO_BOLA = (255, 220, 60)
CORES_BLOCOS = [
    (235, 75, 75),
    (245, 145, 50),
    (240, 210, 60),
    (75, 205, 110),
    (70, 155, 245),
]

fonte = pygame.font.SysFont("arial", 22, bold=True)
fonte_grande = pygame.font.SysFont("arial", 42, bold=True)


def criar_blocos():
  blocos = []
  linhas = 5
  colunas = 8
  largura_bloco = 66
  altura_bloco = 24
  espaco = 6
  margem_x = 15
  margem_y = 65

  for linha in range(linhas):
    for coluna in range(colunas):
      x = margem_x + coluna * (largura_bloco + espaco)
      y = margem_y + linha * (altura_bloco + espaco)
      rect = pygame.Rect(x, y, largura_bloco, altura_bloco)
      blocos.append({"rect": rect, "cor": CORES_BLOCOS[linha]})
  return blocos


def jogar():
  raquete = pygame.Rect(LARGURA // 2 - 55, ALTURA - 45, 110, 14)
  bola = pygame.Rect(LARGURA // 2 - 9, ALTURA - 65, 18, 18)

  vel_bola_x = random.choice([-4, 4])
  vel_bola_y = -5

  blocos = criar_blocos()
  pontos = 0
  vidas = 3
  estado = "JOGANDO"  # JOGANDO, VITORIA, GAMEOVER

  while True:
    for evento in pygame.event.get():
      if evento.type == pygame.QUIT:
        pygame.quit()
        sys.exit()
      if evento.type == pygame.KEYDOWN:
        if evento.key == pygame.K_r and estado != "JOGANDO":
          return

    if estado == "JOGANDO":
      # Movimento da raquete
      teclas = pygame.key.get_pressed()
      if (teclas[pygame.K_LEFT] or teclas[pygame.K_a]) and raquete.left > 0:
        raquete.x -= 8
      if (
          teclas[pygame.K_RIGHT] or teclas[pygame.K_d]
      ) and raquete.right < LARGURA:
        raquete.x += 8

      # Movimento da bola
      bola.x += vel_bola_x
      bola.y += vel_bola_y

      # Colisão com paredes laterais e teto
      if bola.left <= 0 or bola.right >= LARGURA:
        vel_bola_x *= -1
      if bola.top <= 45:
        vel_bola_y *= -1

      # Colisão com a raquete (muda o ângulo conforme onde bate)
      if bola.colliderect(raquete) and vel_bola_y > 0:
        diferenca = (bola.centerx - raquete.centerx) / (raquete.width / 2)
        vel_bola_x = int(diferenca * 6)
        if vel_bola_x == 0:
          vel_bola_x = random.choice([-2, 2])
        vel_bola_y *= -1

      # Colisão com os blocos
      for bloco in blocos[:]:
        if bola.colliderect(bloco["rect"]):
          blocos.remove(bloco)
          vel_bola_y *= -1
          pontos += 10
          break

      # Verificar vitória
      if not blocos:
        estado = "VITORIA"

      # Perder vida se cair
      if bola.top > ALTURA:
        vidas -= 1
        if vidas <= 0:
          estado = "GAMEOVER"
        else:
          bola.center = (raquete.centerx, raquete.top - 15)
          vel_bola_x = random.choice([-4, 4])
          vel_bola_y = -5

    # Desenho
    tela.fill(FUNDO)

    # Barra superior
    pygame.draw.line(tela, (50, 55, 70), (0, 45), (LARGURA, 45), 2)
    txt_pts = fonte.render(f"Pontos: {pontos}", True, BRANCO)
    txt_vidas = fonte.render(f"Vidas: {vidas}", True, BRANCO)
    tela.blit(txt_pts, (15, 10))
    tela.blit(txt_vidas, (LARGURA - 110, 10))

    # Blocos, raquete e bola
    for bloco in blocos:
      pygame.draw.rect(tela, bloco["cor"], bloco["rect"], border_radius=4)

    pygame.draw.rect(tela, AZUL_RAQUETE, raquete, border_radius=6)
    pygame.draw.ellipse(tela, AMARELO_BOLA, bola)

    # Mensagens finais
    if estado != "JOGANDO":
      titulo = "VOCÊ VENCEU!" if estado == "VITORIA" else "GAME OVER"
      cor_titulo = (75, 220, 120) if estado == "VITORIA" else (240, 70, 70)

      txt_fim = fonte_grande.render(titulo, True, cor_titulo)
      txt_reiniciar = fonte.render(
          "Pressione R para jogar novamente", True, BRANCO
      )
      tela.blit(
          txt_fim,
          (LARGURA // 2 - txt_fim.get_width() // 2, ALTURA // 2 - 40),
      )
      tela.blit(
          txt_reiniciar,
          (LARGURA // 2 - txt_reiniciar.get_width() // 2, ALTURA // 2 + 20),
      )

    pygame.display.flip()
    relogio.tick(60)


while True:
  jogar()
