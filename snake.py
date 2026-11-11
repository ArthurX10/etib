import random
import sys
import pygame

# 1. Inicializar o Pygame
pygame.init()

# Configurações da tela e da grade
LARGURA, ALTURA = 600, 600
TAMANHO_BLOCO = 25
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Jogo da Cobrinha")
relogio = pygame.time.Clock()

# Cores
FUNDO_ESCURO = (20, 24, 32)
GRADE_COR = (28, 34, 45)
COBRA_CABECA = (45, 210, 110)
COBRA_CORPO = (30, 165, 85)
COMIDA_COR = (240, 65, 65)
COMIDA_BRILHO = (255, 160, 160)
BRANCO = (245, 245, 245)
AMARELO = (250, 210, 50)
PAINEL_FUNDO = (35, 40, 52)

# Fontes
fonte_placar = pygame.font.SysFont("arial", 22, bold=True)
fonte_titulo = pygame.font.SysFont("arial", 42, bold=True)


def gerar_comida(cobra):
  colunas = LARGURA // TAMANHO_BLOCO
  linhas = ALTURA // TAMANHO_BLOCO
  while True:
    x = random.randint(0, colunas - 1) * TAMANHO_BLOCO
    y = random.randint(2, linhas - 1) * TAMANHO_BLOCO
    if [x, y] not in cobra:
      return [x, y]


def desenhar_grade():
  for x in range(0, LARGURA, TAMANHO_BLOCO):
    pygame.draw.line(tela, GRADE_COR, (x, 50), (x, ALTURA))
  for y in range(50, ALTURA, TAMANHO_BLOCO):
    pygame.draw.line(tela, GRADE_COR, (0, y), (LARGURA, y))


def jogar(recorde_atual):
  # Posição inicial da cobra (3 segmentos no centro)
  inicio_x = (LARGURA // 2 // TAMANHO_BLOCO) * TAMANHO_BLOCO
  inicio_y = (ALTURA // 2 // TAMANHO_BLOCO) * TAMANHO_BLOCO
  cobra = [
      [inicio_x, inicio_y],
      [inicio_x - TAMANHO_BLOCO, inicio_y],
      [inicio_x - 2 * TAMANHO_BLOCO, inicio_y],
  ]

  direcao = "DIREITA"
  proxima_direcao = "DIREITA"
  comida = gerar_comida(cobra)

  pontuacao = 0
  velocidade = 10
  game_over = False

  while True:
    # 2. Eventos
    for evento in pygame.event.get():
      if evento.type == pygame.QUIT:
        pygame.quit()
        sys.exit()

      if evento.type == pygame.KEYDOWN:
        if not game_over:
          if (
              evento.key in (pygame.K_UP, pygame.K_w)
              and direcao != "BAIXO"
          ):
            proxima_direcao = "CIMA"
          elif (
              evento.key in (pygame.K_DOWN, pygame.K_s)
              and direcao != "CIMA"
          ):
            proxima_direcao = "BAIXO"
          elif (
              evento.key in (pygame.K_LEFT, pygame.K_a)
              and direcao != "DIREITA"
          ):
            proxima_direcao = "ESQUERDA"
          elif (
              evento.key in (pygame.K_RIGHT, pygame.K_d)
              and direcao != "ESQUERDA"
          ):
            proxima_direcao = "DIREITA"
        else:
          if evento.key in (pygame.K_r, pygame.K_SPACE):
            return max(pontuacao, recorde_atual)

    # 3. Lógica do jogo
    if not game_over:
      direcao = proxima_direcao
      cabeca_x, cabeca_y = cobra[0]

      if direcao == "CIMA":
        cabeca_y -= TAMANHO_BLOCO
      elif direcao == "BAIXO":
        cabeca_y += TAMANHO_BLOCO
      elif direcao == "ESQUERDA":
        cabeca_x -= TAMANHO_BLOCO
      elif direcao == "DIREITA":
        cabeca_x += TAMANHO_BLOCO

      nova_cabeca = [cabeca_x, cabeca_y]

      # Colisão com as bordas (considerando barra superior de 50px)
      if (
          cabeca_x < 0
          or cabeca_x >= LARGURA
          or cabeca_y < 50
          or cabeca_y >= ALTURA
      ):
        game_over = True

      # Colisão com o próprio corpo
      if nova_cabeca in cobra:
        game_over = True

      if not game_over:
        cobra.insert(0, nova_cabeca)

        # Comer a comida
        if nova_cabeca == comida:
          pontuacao += 10
          comida = gerar_comida(cobra)
          velocidade = min(22, 10 + (pontuacao // 40))
        else:
          cobra.pop()

    # 4. Desenhar na tela
    tela.fill(FUNDO_ESCURO)
    desenhar_grade()

    # Barra superior de pontuação
    pygame.draw.rect(tela, PAINEL_FUNDO, (0, 0, LARGURA, 50))
    pygame.draw.line(tela, GRADE_COR, (0, 50), (LARGURA, 50), 2)

    txt_pontos = fonte_placar.render(f"Pontos: {pontuacao}", True, BRANCO)
    txt_recorde = fonte_placar.render(
        f"Recorde: {max(pontuacao, recorde_atual)}", True, AMARELO
    )
    tela.blit(txt_pontos, (20, 12))
    tela.blit(txt_recorde, (LARGURA - txt_recorde.get_width() - 20, 12))

    # Desenhar comida
    comida_rect = pygame.Rect(
        comida[0] + 2, comida[1] + 2, TAMANHO_BLOCO - 4, TAMANHO_BLOCO - 4
    )
    pygame.draw.rect(tela, COMIDA_COR, comida_rect, border_radius=8)
    pygame.draw.circle(
        tela, COMIDA_BRILHO, (comida[0] + 8, comida[1] + 8), 3
    )

    # Desenhar cobra
    for i, segmento in enumerate(cobra):
      cor = COBRA_CABECA if i == 0 else COBRA_CORPO
      rect = pygame.Rect(
          segmento[0] + 1,
          segmento[1] + 1,
          TAMANHO_BLOCO - 2,
          TAMANHO_BLOCO - 2,
      )
      pygame.draw.rect(tela, cor, rect, border_radius=6)

      # Olhos na cabeça
      if i == 0:
        pygame.draw.circle(
            tela, FUNDO_ESCURO, (segmento[0] + 8, segmento[1] + 8), 3
        )
        pygame.draw.circle(
            tela, FUNDO_ESCURO, (segmento[0] + 17, segmento[1] + 8), 3
        )

    # Tela de Game Over
    if game_over:
      overlay = pygame.Surface((LARGURA, ALTURA - 50), pygame.SRCALPHA)
      overlay.fill((10, 12, 18, 180))
      tela.blit(overlay, (0, 50))

      txt_fim = fonte_titulo.render("FIM DE JOGO", True, COMIDA_COR)
      txt_final = fonte_placar.render(
          f"Pontuação final: {pontuacao}", True, BRANCO
      )
      txt_reiniciar = fonte_placar.render(
          "Aperte R ou ESPAÇO para reiniciar", True, AMARELO
      )

      tela.blit(
          txt_fim,
          (LARGURA // 2 - txt_fim.get_width() // 2, ALTURA // 2 - 60),
      )
      tela.blit(
          txt_final,
          (LARGURA // 2 - txt_final.get_width() // 2, ALTURA // 2),
      )
      tela.blit(
          txt_reiniciar,
          (LARGURA // 2 - txt_reiniciar.get_width() // 2, ALTURA // 2 + 45),
      )

    pygame.display.flip()
    relogio.tick(velocidade)


recorde = 0
while True:
  recorde = jogar(recorde)
