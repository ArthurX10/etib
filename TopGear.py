import random
import sys
import pygame

# 1. Inicializar o Pygame
pygame.init()

# Configurações da tela
LARGURA, ALTURA = 700, 600
HORIZONTE_Y = 230
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Corrida Frontal Pseudo-3D")
relogio = pygame.time.Clock()

# Cores
CEU_TOPO = (30, 60, 130)
CEU_BAIXO = (135, 190, 240)
SOL_COR = (255, 220, 90)
MONTANHA_COR = (55, 75, 110)

GRAMA_CLARA = (45, 165, 70)
GRAMA_ESCURA = (35, 140, 58)
ASFALTO_CLARO = (65, 68, 75)
ASFALTO_ESCURO = (52, 55, 62)
ZEBRADO_VERMELHO = (220, 50, 50)
ZEBRADO_BRANCO = (240, 240, 240)

CARRO_JOGADOR = (0, 170, 255)
VIDRO_ESCURO = (25, 35, 50)
LANTERNA_VERMELHA = (255, 40, 40)
PNEU_COR = (20, 20, 20)
BRANCO = (250, 250, 250)
AMARELO = (255, 215, 50)

CORES_INIMIGOS = [
    (230, 55, 55),
    (245, 140, 35),
    (165, 70, 225),
    (235, 210, 50),
]

fonte_placar = pygame.font.SysFont("arial", 22, bold=True)
fonte_titulo = pygame.font.SysFont("arial", 44, bold=True)


def projetar_ponto(faixa, z):
  """Converte posição lógica (faixa -1, 0, 1 e profundidade z de 0.0 a 1.0) para tela."""
  y = HORIZONTE_Y + (z**1.5) * (ALTURA - HORIZONTE_Y)
  escala = 0.08 + (z**1.5) * 0.92
  largura_pista_no_z = 540 * escala
  x = (LARGURA // 2) + faixa * (largura_pista_no_z * 0.33)
  return x, y, escala


def desenhar_estrada(deslocamento):
  # Céu e Sol
  tela.fill(CEU_BAIXO)
  pygame.draw.rect(tela, CEU_TOPO, (0, 0, LARGURA, HORIZONTE_Y // 2))
  pygame.draw.circle(tela, SOL_COR, (LARGURA - 130, 95), 38)

  # Montanhas no horizonte
  montanhas = [
      (0, HORIZONTE_Y),
      (120, 155),
      (260, HORIZONTE_Y),
      (390, 140),
      (550, HORIZONTE_Y),
      (650, 165),
      (LARGURA, HORIZONTE_Y),
  ]
  pygame.draw.polygon(tela, MONTANHA_COR, montanhas)

  # Desenhar fatias horizontais da estrada do horizonte até a base
  fatias = 55
  for i in range(fatias):
    z1 = i / fatias
    z2 = (i + 1) / fatias

    _, y1, esc1 = projetar_ponto(0, z1)
    _, y2, esc2 = projetar_ponto(0, z2)

    # Alterna cores das faixas para criar sensação de movimento
    faixa_id = int((z1 * 18) - deslocamento) % 2
    cor_grama = GRAMA_CLARA if faixa_id == 0 else GRAMA_ESCURA
    cor_asfalto = ASFALTO_CLARO if faixa_id == 0 else ASFALTO_ESCURO
    cor_borda = ZEBRADO_VERMELHO if faixa_id == 0 else ZEBRADO_BRANCO

    # Grama lateral
    pygame.draw.rect(tela, cor_grama, (0, y1, LARGURA, y2 - y1 + 2))

    # Larguras da pista no topo e na base da fatia
    meia_pista1 = 270 * esc1
    meia_pista2 = 270 * esc2
    borda1 = 22 * esc1
    borda2 = 22 * esc2

    cx = LARGURA // 2

    # Meio-fio (zebrado)
    poly_borda = [
        (cx - meia_pista1 - borda1, y1),
        (cx + meia_pista1 + borda1, y1),
        (cx + meia_pista2 + borda2, y2 + 1),
        (cx - meia_pista2 - borda2, y2 + 1),
    ]
    pygame.draw.polygon(tela, cor_borda, poly_borda)

    # Asfalto
    poly_asfalto = [
        (cx - meia_pista1, y1),
        (cx + meia_pista1, y1),
        (cx + meia_pista2, y2 + 1),
        (cx - meia_pista2, y2 + 1),
    ]
    pygame.draw.polygon(tela, cor_asfalto, poly_asfalto)

    # Linhas divisórias das 3 faixas
    if faixa_id == 0:
      for mult in (-0.165, 0.165):
        lx1 = cx + (meia_pista1 * 2) * mult
        lx2 = cx + (meia_pista2 * 2) * mult
        pygame.draw.line(
            tela, ZEBRADO_BRANCO, (lx1, y1), (lx2, y2), max(1, int(4 * esc2))
        )


def desenhar_carro_traseira(cx, base_y, escala, cor):
  """Desenha um carro visto por trás, escalado conforme a distância."""
  largura = int(125 * escala)
  altura = int(68 * escala)
  if largura < 6 or altura < 4:
    return

  x = int(cx - largura // 2)
  y = int(base_y - altura)

  # Pneus
  larg_pneu = max(3, int(20 * escala))
  alt_pneu = max(3, int(16 * escala))
  pygame.draw.rect(
      tela, PNEU_COR, (x + 4, base_y - alt_pneu + 3, larg_pneu, alt_pneu)
  )
  pygame.draw.rect(
      tela,
      PNEU_COR,
      (x + largura - larg_pneu - 4, base_y - alt_pneu + 3, larg_pneu, alt_pneu),
  )

  # Parte inferior (lataria)
  corpo = pygame.Rect(x, y + int(altura * 0.35), largura, int(altura * 0.65))
  pygame.draw.rect(tela, cor, corpo, border_radius=max(2, int(8 * escala)))

  # Cabine e vidro traseiro
  cabine = pygame.Rect(
      x + int(largura * 0.14),
      y,
      int(largura * 0.72),
      int(altura * 0.45),
  )
  pygame.draw.rect(tela, cor, cabine, border_radius=max(2, int(6 * escala)))

  vidro = pygame.Rect(
      cabine.x + max(2, int(5 * escala)),
      cabine.y + max(2, int(4 * escala)),
      max(2, cabine.width - int(10 * escala)),
      max(2, cabine.height - int(8 * escala)),
  )
  pygame.draw.rect(tela, VIDRO_ESCURO, vidro, border_radius=max(1, int(4 * escala)))

  # Lanternas traseiras
  larg_lanterna = max(2, int(22 * escala))
  alt_lanterna = max(2, int(10 * escala))
  ly = corpo.y + int(corpo.height * 0.25)
  pygame.draw.rect(
      tela, LANTERNA_VERMELHA, (corpo.x + 4, ly, larg_lanterna, alt_lanterna)
  )
  pygame.draw.rect(
      tela,
      LANTERNA_VERMELHA,
      (corpo.right - larg_lanterna - 4, ly, larg_lanterna, alt_lanterna),
  )


def jogar(recorde_atual):
  faixa_alvo = 0  # -1 (esquerda), 0 (centro), 1 (direita)
  faixa_visual = 0.0

  inimigos = []
  tempo_ultimo_inimigo = pygame.time.get_ticks()
  intervalo_inimigos = 1150

  deslocamento_pista = 0.0
  velocidade = 0.014
  pontuacao = 0
  game_over = False

  while True:
    agora = pygame.time.get_ticks()

    # 2. Eventos
    for evento in pygame.event.get():
      if evento.type == pygame.QUIT:
        pygame.quit()
        sys.exit()

      if evento.type == pygame.KEYDOWN:
        if not game_over:
          if evento.key in (pygame.K_LEFT, pygame.K_a) and faixa_alvo > -1:
            faixa_alvo -= 1
          elif evento.key in (pygame.K_RIGHT, pygame.K_d) and faixa_alvo < 1:
            faixa_alvo += 1
        else:
          if evento.key in (pygame.K_r, pygame.K_SPACE):
            return max(pontuacao, recorde_atual)

    # 3. Lógica
    if not game_over:
      # Suavizar troca de faixa
      faixa_visual += (faixa_alvo - faixa_visual) * 0.22

      # Avançar pista e aumentar dificuldade
      velocidade = min(0.028, 0.014 + (pontuacao * 0.00025))
      deslocamento_pista += velocidade * 16

      # Gerar inimigos no horizonte (z = 0.02)
      if agora - tempo_ultimo_inimigo > intervalo_inimigos:
        faixa_inimigo = random.choice([-1, 0, 1])
        inimigos.append({
            "faixa": faixa_inimigo,
            "z": 0.02,
            "cor": random.choice(CORES_INIMIGOS),
        })
        tempo_ultimo_inimigo = agora
        intervalo_inimigos = max(520, 1150 - (pontuacao * 7))

      # Atualizar inimigos
      for carro in inimigos[:]:
        carro["z"] += velocidade

        # Checar colisão quando o carro está na mesma profundidade do jogador
        if 0.84 <= carro["z"] <= 0.96:
          if abs(carro["faixa"] - faixa_visual) < 0.45:
            game_over = True

        # Ultrapassou o jogador
        if carro["z"] > 1.05:
          inimigos.remove(carro)
          pontuacao += 1

    # 4. Desenhar tudo
    desenhar_estrada(deslocamento_pista)

    # Ordenar inimigos do mais distante para o mais próximo (profundidade)
    inimigos_ordenados = sorted(inimigos, key=lambda c: c["z"])
    for carro in inimigos_ordenados:
      ix, iy, iesc = projetar_ponto(carro["faixa"], carro["z"])
      desenhar_carro_traseira(ix, iy, iesc, carro["cor"])

    # Desenhar carro do jogador perto da base da tela (z = 0.90)
    jx, jy, jesc = projetar_ponto(faixa_visual, 0.90)
    desenhar_carro_traseira(jx, jy, jesc, CARRO_JOGADOR)

    # Placar
    painel = pygame.Rect(15, 15, LARGURA - 30, 42)
    pygame.draw.rect(tela, (20, 25, 35), painel, border_radius=8)
    txt_pts = fonte_placar.render(f"Ultrapassagens: {pontuacao}", True, BRANCO)
    txt_rec = fonte_placar.render(
        f"Recorde: {max(pontuacao, recorde_atual)}", True, AMARELO
    )
    tela.blit(txt_pts, (30, 23))
    tela.blit(txt_rec, (LARGURA - txt_rec.get_width() - 30, 23))

    # Tela de Game Over
    if game_over:
      overlay = pygame.Surface((LARGURA, ALTURA), pygame.SRCALPHA)
      overlay.fill((10, 12, 18, 175))
      tela.blit(overlay, (0, 0))

      txt_fim = fonte_titulo.render("BATIDA!", True, (245, 70, 70))
      txt_rst = fonte_placar.render(
          "Aperte R ou ESPAÇO para correr novamente", True, AMARELO
      )
      tela.blit(
          txt_fim,
          (LARGURA // 2 - txt_fim.get_width() // 2, ALTURA // 2 - 45),
      )
      tela.blit(
          txt_rst,
          (LARGURA // 2 - txt_rst.get_width() // 2, ALTURA // 2 + 15),
      )

    pygame.display.flip()
    relogio.tick(60)


recorde = 0
while True:
  recorde = jogar(recorde)

