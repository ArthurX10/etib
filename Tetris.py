import random
import sys
import pygame

pygame.init()

# Configurações da tela e do tabuleiro
LARGURA_TELA, ALTURA_TELA = 600, 700
TAMANHO_BLOCO = 30
COLUNAS = 10
LINHAS = 20
LARGURA_TABULEIRO = COLUNAS * TAMANHO_BLOCO
ALTURA_TABULEIRO = LINHAS * TAMANHO_BLOCO
OFFSET_X = (LARGURA_TELA - LARGURA_TABULEIRO) // 2
OFFSET_Y = 50

tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
pygame.display.set_caption("Tetris - Pygame")
relogio = pygame.time.Clock()

# Cores
FUNDO = (20, 24, 33)
PAINEL = (30, 36, 48)
BRANCO = (240, 240, 240)
GRADE = (40, 48, 64)

CORES_PECAS = {
    "I": (0, 240, 240),
    "O": (240, 240, 0),
    "T": (160, 32, 240),
    "S": (0, 240, 0),
    "Z": (240, 0, 0),
    "J": (0, 0, 240),
    "L": (240, 160, 0),
}

PECAS = {
    "I": [[1, 1, 1, 1]],
    "O": [[1, 1], [1, 1]],
    "T": [[0, 1, 0], [1, 1, 1]],
    "S": [[0, 1, 1], [1, 1, 0]],
    "Z": [[1, 1, 0], [0, 1, 1]],
    "J": [[1, 0, 0], [1, 1, 1]],
    "L": [[0, 0, 1], [1, 1, 1]],
}

fonte_titulo = pygame.font.SysFont("arial", 32, bold=True)
fonte_ui = pygame.font.SysFont("arial", 20, bold=True)


class Peca:

  def __init__(self, tipo):
    self.tipo = tipo
    self.forma = PECAS[tipo]
    self.cor = CORES_PECAS[tipo]
    self.x = COLUNAS // 2 - len(self.forma[0]) // 2
    self.y = 0


def criar_grade():
  return [[None for _ in range(COLUNAS)] for _ in range(LINHAS)]


def colide(grade, peca, dx=0, dy=0, forma=None):
  f = forma if forma else peca.forma
  for y, linha in enumerate(f):
    for x, celula in enumerate(linha):
      if celula:
        novo_x = peca.x + x + dx
        novo_y = peca.y + y + dy
        if novo_x < 0 or novo_x >= COLUNAS or novo_y >= LINHAS:
          return True
        if novo_y >= 0 and grade[novo_y][novo_x] is not None:
          return True
  return False


def fixar_peca(grade, peca):
  for y, linha in enumerate(peca.forma):
    for x, celula in enumerate(linha):
      if celula:
        if peca.y + y < 0:
          return False
        grade[peca.y + y][peca.x + x] = peca.cor
  return True


def limpar_linhas(grade):
  novas_linhas = [linha for linha in grade if None in linha]
  linhas_removidas = LINHAS - len(novas_linhas)
  while len(novas_linhas) < LINHAS:
    novas_linhas.insert(0, [None for _ in range(COLUNAS)])
  return novas_linhas, linhas_removidas


def rotacionar(peca):
  nova_forma = list(zip(*peca.forma[::-1]))
  if not colide(grade_atual, peca, forma=nova_forma):
    peca.forma = nova_forma


def jogar():
  global grade_atual
  grade_atual = criar_grade()
  peca_atual = Peca(random.choice(list(PECAS.keys())))
  proxima_peca = Peca(random.choice(list(PECAS.keys())))

  pontos = 0
  linhas_total = 0
  nivel = 1
  game_over = False

  tempo_queda = 0
  velocidade = 500  # milissegundos

  while True:
    dt = relogio.tick(60)
    tempo_queda += dt

    for evento in pygame.event.get():
      if evento.type == pygame.QUIT:
        pygame.quit()
        sys.exit()

      if not game_over:
        if evento.type == pygame.KEYDOWN:
          if evento.key == pygame.K_LEFT and not colide(
              grade_atual, peca_atual, dx=-1
          ):
            peca_atual.x -= 1
          elif evento.key == pygame.K_RIGHT and not colide(
              grade_atual, peca_atual, dx=1
          ):
            peca_atual.x += 1
          elif evento.key == pygame.K_DOWN and not colide(
              grade_atual, peca_atual, dy=1
          ):
            peca_atual.y += 1
          elif evento.key == pygame.K_UP:
            rotacionar(peca_atual)
          elif evento.key == pygame.K_SPACE:
            while not colide(grade_atual, peca_atual, dy=1):
              peca_atual.y += 1
            fixar_peca(grade_atual, peca_atual)
            grade_atual, r = limpar_linhas(grade_atual)
            if r > 0:
              linhas_total += r
              pontos += (r**2) * 100
              nivel = linhas_total // 5 + 1
              velocidade = max(100, 500 - (nivel - 1) * 60)
            peca_atual = proxima_peca
            proxima_peca = Peca(random.choice(list(PECAS.keys())))
            if colide(grade_atual, peca_atual):
              game_over = True
      else:
        if evento.type == pygame.KEYDOWN and evento.key == pygame.K_r:
          return

    if not game_over and tempo_queda > velocidade:
      if not colide(grade_atual, peca_atual, dy=1):
        peca_atual.y += 1
      else:
        if not fixar_peca(grade_atual, peca_atual):
          game_over = True
        else:
          grade_atual, r = limpar_linhas(grade_atual)
          if r > 0:
            linhas_total += r
            pontos += (r**2) * 100
            nivel = linhas_total // 5 + 1
            velocidade = max(100, 500 - (nivel - 1) * 60)
          peca_atual = proxima_peca
          proxima_peca = Peca(random.choice(list(PECAS.keys())))
          if colide(grade_atual, peca_atual):
            game_over = True
      tempo_queda = 0

    # Desenho
    tela.fill(FUNDO)

    # Painel lateral esquerdo (Pontuação)
    pygame.draw.rect(
        tela, PAINEL, (OFFSET_X - 160, OFFSET_Y, 140, 200), border_radius=10
    )
    txt_pt_tit = fonte_ui.render("PONTOS", True, BRANCO)
    txt_pt_val = fonte_ui.render(str(pontos), True, CORES_PECAS["T"])
    txt_nv_tit = fonte_ui.render("NÍVEL", True, BRANCO)
    txt_nv_val = fonte_ui.render(str(nivel), True, CORES_PECAS["O"])
    tela.blit(txt_pt_tit, (OFFSET_X - 145, OFFSET_Y + 15))
    tela.blit(txt_pt_val, (OFFSET_X - 145, OFFSET_Y + 45))
    tela.blit(txt_nv_tit, (OFFSET_X - 145, OFFSET_Y + 105))
    tela.blit(txt_nv_val, (OFFSET_X - 145, OFFSET_Y + 135))

    # Moldura do tabuleiro
    pygame.draw.rect(
        tela,
        PAINEL,
        (
            OFFSET_X - 2,
            OFFSET_Y - 2,
            LARGURA_TABULEIRO + 4,
            ALTURA_TABULEIRO + 4,
        ),
        border_radius=6,
    )
    pygame.draw.rect(
        tela,
        (0, 0, 0),
        (OFFSET_X, OFFSET_Y, LARGURA_TABULEIRO, ALTURA_TABULEIRO),
    )

    # Desenhar grade de blocos fixados
    for y in range(LINHAS):
      for x in range(COLUNAS):
        cor = grade_atual[y][x]
        rect_bloco = pygame.Rect(
            OFFSET_X + x * TAMANHO_BLOCO,
            OFFSET_Y + y * TAMANHO_BLOCO,
            TAMANHO_BLOCO - 1,
            TAMANHO_BLOCO - 1,
        )
        if cor:
          pygame.draw.rect(tela, cor, rect_bloco, border_radius=3)
        else:
          pygame.draw.rect(tela, GRADE, rect_bloco, 1)

    # Desenhar peça atual
    if not game_over:
      for y, linha in enumerate(peca_atual.forma):
        for x, celula in enumerate(linha):
          if celula:
            rx = OFFSET_X + (peca_atual.x + x) * TAMANHO_BLOCO
            ry = OFFSET_Y + (peca_atual.y + y) * TAMANHO_BLOCO
            if ry >= OFFSET_Y:
              pygame.draw.rect(
                  tela,
                  peca_atual.cor,
                  (rx, ry, TAMANHO_BLOCO - 1, TAMANHO_BLOCO - 1),
                  border_radius=3,
              )

    if game_over:
      txt_go = fonte_titulo.render("FIM DE JOGO", True, (240, 50, 50))
      txt_res = fonte_ui.render("Aperte R para recomeçar", True, BRANCO)
      tela.blit(
          txt_go,
          (
              OFFSET_X + LARGURA_TABULEIRO // 2 - txt_go.get_width() // 2,
              OFFSET_Y + ALTURA_TABULEIRO // 2 - 30,
          ),
      )
      tela.blit(
          txt_res,
          (
              OFFSET_X + LARGURA_TABULEIRO // 2 - txt_res.get_width() // 2,
              OFFSET_Y + ALTURA_TABULEIRO // 2 + 15,
          ),
      )

    pygame.display.flip()


while True:
  jogar()
