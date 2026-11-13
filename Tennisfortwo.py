"""Tennis for Two (1958)

Recriação de um dos primeiros videogames da história, criado pelo físico
William Higinbotham no Brookhaven National Laboratory (EUA). O original
rodava em um computador analógico e era exibido em um osciloscópio.

A quadra é vista de lado: a bola descreve uma parábola (gravidade),
quica no chão e precisa passar por cima da rede. Cada jogador tem um
"botão giratório" para escolher o ângulo da raquetada e um botão para bater.
"""

import math
import sys
import pygame

# 1. Inicializar o Pygame
pygame.init()

# Configurações da tela
LARGURA, ALTURA = 900, 560
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Tennis for Two (1958)")
relogio = pygame.time.Clock()

# Cores (fósforo verde de osciloscópio)
FUNDO = (3, 12, 7)
GRADE_COR = (10, 34, 20)
GRADE_CENTRO = (16, 56, 32)
VERDE = (110, 255, 150)
VERDE_MEDIO = (60, 190, 100)
VERDE_ESCURO = (30, 120, 60)
AMARELO = (240, 230, 120)

# Fontes
fonte_placar = pygame.font.SysFont("consolas,couriernew,monospace", 24, bold=True)
fonte_texto = pygame.font.SysFont("consolas,couriernew,monospace", 16, bold=True)
fonte_titulo = pygame.font.SysFont("consolas,couriernew,monospace", 38, bold=True)

# Quadra (em pixels)
CHAO_Y = 470
REDE_X = LARGURA // 2
REDE_ALTURA = 55
LIMITE_ESQ = 40
LIMITE_DIR = LARGURA - 40

# Física
GRAVIDADE = 620            # px/s²
VELOCIDADE_BATIDA = 560    # px/s (a velocidade da raquetada é sempre a mesma)
COEF_QUICA = 0.78          # fração da velocidade vertical mantida após quicar
ATRITO_QUICA = 0.92        # fração da velocidade horizontal mantida após quicar
RAIO_BOLA = 5

# Controles
ANGULO_MIN = 10
ANGULO_MAX = 80
VELOCIDADE_ANGULO = 45     # graus por segundo girando o "botão"
PONTOS_VITORIA = 7
TEMPO_MENSAGEM = 1.7       # segundos mostrando o resultado do ponto

# Teclas: Jogador 1 (esquerda) e Jogador 2 (direita)
TECLAS = {
    1: {"sobe": pygame.K_w, "desce": pygame.K_s, "bater": pygame.K_d},
    2: {"sobe": pygame.K_UP, "desce": pygame.K_DOWN, "bater": pygame.K_LEFT},
}

# Brilho (halo) da bola, criado uma vez só
brilho = pygame.Surface((48, 48), pygame.SRCALPHA)
for raio, alfa in ((22, 18), (16, 32), (11, 60), (7, 110)):
  pygame.draw.circle(brilho, (*VERDE, alfa), (24, 24), raio)


def outro(jogador):
  return 2 if jogador == 1 else 1


def lado_da_bola(bola):
  return 1 if bola["x"] < REDE_X else 2


def quem_pode_bater(bola, fase, sacador):
  """Retorna o jogador que pode bater agora (ou None).

  As batidas são alternadas: quem acabou de bater não pode bater de novo
  até o adversário devolver.
  """
  if bola["recarga"] > 0:
    return None
  if fase == "saque":
    return sacador
  if fase == "jogo" and bola["ultimo"] != lado_da_bola(bola):
    return lado_da_bola(bola)
  return None


def nova_bola_saque(sacador):
  x = LIMITE_ESQ + 70 if sacador == 1 else LIMITE_DIR - 70
  return {
      "x": x,
      "y": CHAO_Y - 70,
      "vx": 0.0,
      "vy": 0.0,
      "ultimo": sacador,   # quem bateu por último
      "quiques": 0,        # quiques no lado do adversário desde a última batida
      "recarga": 0.0,      # tempo até poder bater de novo
  }


def bater(bola, jogador, angulo):
  """A raquetada: velocidade fixa, direção dada pelo ângulo do botão."""
  rad = math.radians(angulo)
  direcao = 1 if jogador == 1 else -1
  bola["vx"] = direcao * VELOCIDADE_BATIDA * math.cos(rad)
  bola["vy"] = -VELOCIDADE_BATIDA * math.sin(rad)
  bola["ultimo"] = jogador
  bola["quiques"] = 0
  bola["recarga"] = 0.3


def passou_pela_rede(x_antes, x_depois):
  return x_antes != x_depois and (x_antes - REDE_X) * (x_depois - REDE_X) <= 0


def atualizar_bola(bola, dt):
  """Move a bola. Retorna (vencedor, motivo) se o ponto terminou."""
  bola["recarga"] = max(0.0, bola["recarga"] - dt)
  passos = 4  # dividir o tempo em passos menores deixa a física mais estável
  h = dt / passos

  for _ in range(passos):
    x_antes = bola["x"]
    bola["vy"] += GRAVIDADE * h
    bola["x"] += bola["vx"] * h
    bola["y"] += bola["vy"] * h

    # Bateu na rede?
    topo_rede = CHAO_Y - REDE_ALTURA
    if passou_pela_rede(x_antes, bola["x"]) and bola["y"] + RAIO_BOLA > topo_rede:
      return outro(bola["ultimo"]), "Na rede!"

    # Quicou no chão?
    if bola["y"] + RAIO_BOLA >= CHAO_Y and bola["vy"] > 0:
      bola["y"] = CHAO_Y - RAIO_BOLA
      bola["vy"] = -bola["vy"] * COEF_QUICA
      bola["vx"] *= ATRITO_QUICA
      if lado_da_bola(bola) == bola["ultimo"]:
        return outro(bola["ultimo"]), "Quicou no próprio lado!"
      bola["quiques"] += 1
      if bola["quiques"] >= 2:
        return bola["ultimo"], "Bola não devolvida!"

    # Saiu da quadra?
    if bola["x"] < LIMITE_ESQ or bola["x"] > LIMITE_DIR:
      if lado_da_bola(bola) != bola["ultimo"] and bola["quiques"] >= 1:
        return bola["ultimo"], "Bola não devolvida!"
      return outro(bola["ultimo"]), "Bola fora!"

  return None


def pontos_da_trajetoria(bola, jogador, angulo):
  """Pontos da parábola prevista (guia opcional, tecla G)."""
  rad = math.radians(angulo)
  direcao = 1 if jogador == 1 else -1
  vx = direcao * VELOCIDADE_BATIDA * math.cos(rad)
  vy = -VELOCIDADE_BATIDA * math.sin(rad)
  pontos = []
  t = 0.0
  while t < 3:
    x = bola["x"] + vx * t
    y = bola["y"] + vy * t + 0.5 * GRAVIDADE * t * t
    if y > CHAO_Y or x < LIMITE_ESQ or x > LIMITE_DIR:
      break
    pontos.append((x, y))
    t += 0.04
  return pontos


def texto_centralizado(texto, fonte, cor, y):
  img = fonte.render(texto, True, cor)
  tela.blit(img, (LARGURA // 2 - img.get_width() // 2, y))


def desenhar_grade():
  """Quadriculado de fundo, como a tela de um osciloscópio."""
  for i in range(0, LARGURA + 1, LARGURA // 10):
    cor = GRADE_CENTRO if i == LARGURA // 2 else GRADE_COR
    pygame.draw.line(tela, cor, (i, 0), (i, ALTURA))
  for j in range(0, ALTURA + 1, ALTURA // 8):
    cor = GRADE_CENTRO if j == ALTURA // 2 else GRADE_COR
    pygame.draw.line(tela, cor, (0, j), (LARGURA, j))


def desenhar_quadra():
  pygame.draw.line(tela, VERDE, (LIMITE_ESQ - 20, CHAO_Y), (LIMITE_DIR + 20, CHAO_Y), 2)
  pygame.draw.line(
      tela, VERDE, (REDE_X, CHAO_Y), (REDE_X, CHAO_Y - REDE_ALTURA), 3
  )
  for x in (LIMITE_ESQ, LIMITE_DIR):
    pygame.draw.line(tela, VERDE_MEDIO, (x, CHAO_Y), (x, CHAO_Y + 10), 2)


def desenhar_botao(jogador, angulo, ativo):
  """Mostra o 'botão giratório' (mostrador de ângulo) de cada jogador."""
  cx = 90 if jogador == 1 else LARGURA - 90
  cy = ALTURA - 38
  cor = VERDE if ativo else VERDE_ESCURO
  direcao = 1 if jogador == 1 else -1
  pygame.draw.arc(
      tela, VERDE_ESCURO, (cx - 34, cy - 34, 68, 68),
      0 if jogador == 1 else math.pi / 2,
      math.pi / 2 if jogador == 1 else math.pi, 2,
  )
  rad = math.radians(angulo)
  ponta = (cx + direcao * 34 * math.cos(rad), cy - 34 * math.sin(rad))
  pygame.draw.line(tela, cor, (cx, cy), ponta, 3)
  pygame.draw.circle(tela, cor, (cx, cy), 4)
  txt = fonte_texto.render(f"J{jogador}  {int(angulo)}°", True, cor)
  deslocamento = 48 if jogador == 1 else -48 - txt.get_width()
  tela.blit(txt, (cx + deslocamento, cy - 20))


def desenhar_bola(bola, rastro):
  total = len(rastro)
  for i, (x, y) in enumerate(rastro):
    k = (i + 1) / total
    cor = (int(VERDE[0] * k * 0.6), int(VERDE[1] * k * 0.6), int(VERDE[2] * k * 0.6))
    pygame.draw.circle(tela, cor, (int(x), int(y)), 2)
  tela.blit(brilho, (bola["x"] - 24, bola["y"] - 24))
  pygame.draw.circle(tela, VERDE, (int(bola["x"]), int(bola["y"])), RAIO_BOLA)


def jogar():
  pontos = {1: 0, 2: 0}
  angulos = {1: 45.0, 2: 45.0}
  sacador = 1
  bola = nova_bola_saque(sacador)
  rastro = []
  fase = "saque"     # saque -> jogo -> ponto -> saque ... -> fim
  mensagem = ""
  tempo_mensagem = 0.0
  mostrar_guia = False

  while True:
    dt = min(relogio.tick(120) / 1000, 0.05)

    for evento in pygame.event.get():
      if evento.type == pygame.QUIT:
        pygame.quit()
        sys.exit()
      if evento.type == pygame.KEYDOWN:
        if evento.key == pygame.K_ESCAPE:
          pygame.quit()
          sys.exit()
        if evento.key == pygame.K_g:
          mostrar_guia = not mostrar_guia
        if evento.key == pygame.K_r and fase == "fim":
          return
        for jogador in (1, 2):
          if evento.key != TECLAS[jogador]["bater"]:
            continue
          if quem_pode_bater(bola, fase, sacador) == jogador:
            bater(bola, jogador, angulos[jogador])
            fase = "jogo"

    # Girar os botões de ângulo
    teclas = pygame.key.get_pressed()
    for jogador in (1, 2):
      if teclas[TECLAS[jogador]["sobe"]]:
        angulos[jogador] += VELOCIDADE_ANGULO * dt
      if teclas[TECLAS[jogador]["desce"]]:
        angulos[jogador] -= VELOCIDADE_ANGULO * dt
      angulos[jogador] = max(ANGULO_MIN, min(ANGULO_MAX, angulos[jogador]))

    # Lógica
    if fase == "jogo":
      resultado = atualizar_bola(bola, dt)
      rastro.append((bola["x"], bola["y"]))
      rastro = rastro[-70:]
      if resultado:
        vencedor, mensagem = resultado
        pontos[vencedor] += 1
        mensagem = f"{mensagem}  Ponto do Jogador {vencedor}"
        tempo_mensagem = TEMPO_MENSAGEM
        fase = "fim" if pontos[vencedor] >= PONTOS_VITORIA else "ponto"
        if fase == "fim":
          mensagem = f"JOGADOR {vencedor} VENCEU!"
    elif fase == "ponto":
      tempo_mensagem -= dt
      if tempo_mensagem <= 0:
        sacador = outro(sacador)
        bola = nova_bola_saque(sacador)
        rastro = []
        fase = "saque"

    # Desenho
    tela.fill(FUNDO)
    desenhar_grade()
    desenhar_quadra()

    texto_centralizado("TENNIS FOR TWO", fonte_texto, VERDE_MEDIO, 12)
    texto_centralizado(
        f"J1  {pontos[1]}  x  {pontos[2]}  J2", fonte_placar, VERDE, 36
    )

    desenhar_bola(bola, rastro)

    # Anel indica quem pode bater agora
    quem = quem_pode_bater(bola, fase, sacador)
    if quem:
      pygame.draw.circle(
          tela, AMARELO, (int(bola["x"]), int(bola["y"])), RAIO_BOLA + 9, 1
      )
      if mostrar_guia:
        for px, py in pontos_da_trajetoria(bola, quem, angulos[quem]):
          pygame.draw.circle(tela, VERDE_ESCURO, (int(px), int(py)), 2)

    desenhar_botao(1, angulos[1], quem == 1)
    desenhar_botao(2, angulos[2], quem == 2)

    if fase == "saque":
      texto_centralizado(
          f"Jogador {sacador} saca: ajuste o ângulo e bata!", fonte_texto, AMARELO, 90
      )
    elif fase == "ponto":
      texto_centralizado(mensagem, fonte_placar, AMARELO, 90)
    elif fase == "fim":
      texto_centralizado(mensagem, fonte_titulo, AMARELO, ALTURA // 2 - 70)
      texto_centralizado(
          "Aperte R para jogar de novo", fonte_placar, VERDE, ALTURA // 2 - 20
      )

    texto_centralizado(
        "J1: W/S ângulo, D bate | J2: cima/baixo ângulo, esquerda bate | G: guia",
        fonte_texto, VERDE_ESCURO, ALTURA - 24,
    )

    pygame.display.flip()


while True:
  jogar()
