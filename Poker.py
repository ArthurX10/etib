from collections import Counter
from itertools import combinations
import random
import sys
import pygame

pygame.init()

# Configurações da tela
LARGURA, ALTURA = 900, 620
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Texas Hold'em Poker - Você vs Bot")
relogio = pygame.time.Clock()

# Cores
MESA_VERDE = (24, 112, 62)
MESA_BORDA = (15, 72, 39)
CARTA_FRENTE = (248, 248, 248)
CARTA_VERSO = (35, 80, 165)
VERMELHO = (210, 35, 45)
PRETO = (25, 25, 30)
OURO = (245, 195, 45)
BRANCO = (250, 250, 250)
BOTAO_VERMELHO = (195, 55, 55)
BOTAO_AZUL = (40, 125, 210)
BOTAO_VERDE = (40, 175, 85)
BOTAO_CINZA = (85, 95, 90)
PAINEL_ESCURO = (18, 55, 34)

# Fontes
fonte_carta_grande = pygame.font.SysFont("arial", 30, bold=True)
fonte_carta_peq = pygame.font.SysFont("arial", 19, bold=True)
fonte_ui = pygame.font.SysFont("arial", 20, bold=True)
fonte_titulo = pygame.font.SysFont("arial", 24, bold=True)

NAIPES = ("♠", "♥", "♦", "♣")
VALORES = tuple(range(2, 15))
NOMES_VALORES = {
    11: "J",
    12: "Q",
    13: "K",
    14: "A",
}

NOMES_MAOS = {
    8: "Straight Flush",
    7: "Quadra",
    6: "Full House",
    5: "Flush",
    4: "Sequência",
    3: "Trinca",
    2: "Dois Pares",
    1: "Um Par",
    0: "Carta Alta",
}


def criar_baralho():
  baralho = [(v, n) for v in VALORES for n in NAIPES]
  random.shuffle(baralho)
  return baralho


def texto_valor(valor):
  return NOMES_VALORES.get(valor, str(valor))


def pontuar_5_cartas(cinco_cartas):
  valores = tuple(sorted((c[0] for c in cinco_cartas), reverse=True))
  naipes = tuple(c[1] for c in cinco_cartas)

  mesmo_naipe = len(set(naipes)) == 1
  valores_asc = tuple(sorted(valores))
  menor = valores_asc[0]

  sequencia = False
  alto_seq = valores[0]
  if valores_asc == tuple(range(menor, menor + 5)):
    sequencia = True
    alto_seq = valores_asc[4]
  elif valores_asc == (2, 3, 4, 5, 14):
    sequencia = True
    alto_seq = 5

  contagem_dict = Counter(valores)
  grupos = sorted(
      contagem_dict.items(), key=lambda x: (x[1], x[0]), reverse=True
  )
  qtds = tuple(g[1] for g in grupos)
  vals_ordenados = tuple(g[0] for g in grupos)

  if mesmo_naipe and sequencia:
    return (8, alto_seq)
  if qtds == (4, 1):
    return (7,) + vals_ordenados
  if qtds == (3, 2):
    return (6,) + vals_ordenados
  if mesmo_naipe:
    return (5,) + valores
  if sequencia:
    return (4, alto_seq)
  if qtds == (3, 1, 1):
    return (3,) + vals_ordenados
  if qtds == (2, 2, 1):
    return (2,) + vals_ordenados
  if qtds == (2, 1, 1, 1):
    return (1,) + vals_ordenados
  return (0,) + valores


def melhor_mao_7_cartas(sete_cartas):
  melhor_score = (-1,)
  for comb in combinations(sete_cartas, 5):
    score = pontuar_5_cartas(comb)
    if score > melhor_score:
      melhor_score = score
  return melhor_score


def desenhar_carta(rect, carta, revelada=True):
  if not revelada:
    pygame.draw.rect(tela, CARTA_VERSO, rect, border_radius=8)
    pygame.draw.rect(tela, BRANCO, rect, 2, border_radius=8)
    interno = rect.inflate(-14, -14)
    pygame.draw.rect(tela, (25, 60, 130), interno, border_radius=5)
    return

  pygame.draw.rect(tela, CARTA_FRENTE, rect, border_radius=8)
  pygame.draw.rect(tela, PRETO, rect, 2, border_radius=8)

  valor, naipe = carta
  cor = VERMELHO if naipe in ("♥", "♦") else PRETO
  str_v = texto_valor(valor)

  txt_topo = fonte_carta_peq.render(f"{str_v}{naipe}", True, cor)
  txt_centro = fonte_carta_grande.render(naipe, True, cor)

  tela.blit(txt_topo, (rect.x + 8, rect.y + 6))
  tela.blit(
      txt_centro,
      (
          rect.centerx - txt_centro.get_width() // 2,
          rect.centery - txt_centro.get_height() // 2 + 4,
      ),
  )


def desenhar_botao(rect, texto, cor, ativo=True):
  cor_final = cor if ativo else BOTAO_CINZA
  pygame.draw.rect(tela, cor_final, rect, border_radius=8)
  pygame.draw.rect(tela, BRANCO, rect, 2, border_radius=8)
  txt = fonte_ui.render(texto, True, BRANCO)
  tela.blit(
      txt,
      (rect.centerx - txt.get_width() // 2, rect.centery - txt.get_height() // 2),
  )


def iniciar_mao(f_jog, f_bot, blind=20):
  baralho = criar_baralho()
  mao_j = [baralho.pop(), baralho.pop()]
  mao_b = [baralho.pop(), baralho.pop()]
  mesa = [baralho.pop() for _ in range(5)]

  aposta_j = min(blind, f_jog)
  aposta_b = min(blind, f_bot)
  f_jog -= aposta_j
  f_bot -= aposta_b
  pote = aposta_j + aposta_b

  return {
      "mao_j": mao_j,
      "mao_b": mao_b,
      "mesa": mesa,
      "cartas_visiveis": 0,
      "fase": "PRE-FLOP",
      "fichas_j": f_jog,
      "fichas_b": f_bot,
      "pote": pote,
      "status": "Sua vez: Pagar/Passar ou Apostar +20",
      "acao_bot": "Bot pagou o blind (20)",
      "fim_rodada": False,
  }


def avancar_fase(est):
  if est["fase"] == "PRE-FLOP":
    est["fase"] = "FLOP"
    est["cartas_visiveis"] = 3
  elif est["fase"] == "FLOP":
    est["fase"] = "TURN"
    est["cartas_visiveis"] = 4
  elif est["fase"] == "TURN":
    est["fase"] = "RIVER"
    est["cartas_visiveis"] = 5
  elif est["fase"] == "RIVER":
    est["fase"] = "SHOWDOWN"
    est["fim_rodada"] = True
    score_j = melhor_mao_7_cartas(est["mao_j"] + est["mesa"])
    score_b = melhor_mao_7_cartas(est["mao_b"] + est["mesa"])

    nome_j = NOMES_MAOS[score_j[0]]
    nome_b = NOMES_MAOS[score_b[0]]

    if score_j > score_b:
      est["fichas_j"] += est["pote"]
      est["status"] = f"Você venceu ({nome_j} vs {nome_b})! +{est['pote']} fichas"
    elif score_b > score_j:
      est["fichas_b"] += est["pote"]
      est["status"] = f"Bot venceu ({nome_b} vs {nome_j})!"
    else:
      metade = est["pote"] // 2
      est["fichas_j"] += metade
      est["fichas_b"] += est["pote"] - metade
      est["status"] = f"Empate ({nome_j})! Pote dividido."
    est["pote"] = 0


def turno_bot(est, valor_raise):
  cartas_bot_atuais = est["mao_b"] + est["mesa"][: est["cartas_visiveis"]]
  forca_par = est["mao_b"][0][0] == est["mao_b"][1][0]
  carta_alta = max(est["mao_b"][0][0], est["mao_b"][1][0]) >= 11

  if valor_raise > 0:
    chance_pagar = 0.85 if (forca_par or carta_alta or len(cartas_bot_atuais) >= 5) else 0.45
    if random.random() < chance_pagar:
      pago = min(valor_raise, est["fichas_b"])
      est["fichas_b"] -= pago
      est["pote"] += pago
      est["acao_bot"] = f"Bot pagou +{pago} fichas"
      avancar_fase(est)
    else:
      est["fichas_j"] += est["pote"]
      est["pote"] = 0
      est["acao_bot"] = "Bot desistiu (Fold)!"
      est["status"] = "Você venceu a mão! O Bot correu."
      est["fim_rodada"] = True
  else:
    if est["fichas_b"] >= 20 and random.random() < 0.25:
      aposta_b = min(20, est["fichas_b"])
      est["fichas_b"] -= aposta_b
      est["pote"] += aposta_b
      pago_j = min(aposta_b, est["fichas_j"])
      est["fichas_j"] -= pago_j
      est["pote"] += pago_j
      est["acao_bot"] = f"Bot apostou {aposta_b} e você cobriu"
    else:
      est["acao_bot"] = "Bot deu Check (passou)"
    avancar_fase(est)


def desenhar_tela(est, btn_fold, btn_call, btn_raise, btn_nova):
  tela.fill(MESA_BORDA)
  pygame.draw.rect(
      tela, MESA_VERDE, (18, 18, LARGURA - 36, ALTURA - 36), border_radius=24
  )

  # Painel superior (Bot)
  painel_bot = pygame.Rect(40, 30, LARGURA - 80, 145)
  pygame.draw.rect(tela, PAINEL_ESCURO, painel_bot, border_radius=12)

  txt_bot = fonte_ui.render(f"BOT  |  Fichas: {est['fichas_b']}", True, BRANCO)
  txt_acao_b = fonte_ui.render(est["acao_bot"], True, OURO)
  tela.blit(txt_bot, (60, 42))
  tela.blit(txt_acao_b, (LARGURA - txt_acao_b.get_width() - 60, 42))

  # Cartas do Bot
  for i in range(2):
    rect_b = pygame.Rect(LARGURA // 2 - 95 + i * 100, 72, 85, 95)
    desenhar_carta(rect_b, est["mao_b"][i], revelada=est["fim_rodada"])

  # Cartas Comunitárias (Mesa) e Pote
  txt_pote = fonte_titulo.render(
      f"POTE: {est['pote']} fichas  ({est['fase']})", True, OURO
  )
  tela.blit(txt_pote, (LARGURA // 2 - txt_pote.get_width() // 2, 195))

  inicio_mesa_x = (LARGURA - (5 * 95 + 4 * 15)) // 2
  for i in range(5):
    rect_m = pygame.Rect(inicio_mesa_x + i * 110, 235, 95, 130)
    if i < est["cartas_visiveis"]:
      desenhar_carta(rect_m, est["mesa"][i], revelada=True)
    else:
      pygame.draw.rect(tela, PAINEL_ESCURO, rect_m, border_radius=8)
      pygame.draw.rect(tela, (40, 140, 80), rect_m, 2, border_radius=8)

  # Mensagem central de status
  txt_status = fonte_ui.render(est["status"], True, BRANCO)
  tela.blit(txt_status, (LARGURA // 2 - txt_status.get_width() // 2, 382))

  # Área do Jogador
  for i in range(2):
    rect_j = pygame.Rect(LARGURA // 2 - 95 + i * 100, 415, 85, 105)
    desenhar_carta(rect_j, est["mao_j"][i], revelada=True)

  txt_jog = fonte_ui.render(f"VOCÊ  |  Fichas: {est['fichas_j']}", True, OURO)
  tela.blit(txt_jog, (55, 455))

  # Botões de controle
  if not est["fim_rodada"]:
    desenhar_botao(btn_fold, "DESISTIR", BOTAO_VERMELHO, True)
    desenhar_botao(btn_call, "PASSAR / PAGAR", BOTAO_AZUL, True)
    desenhar_botao(btn_raise, "APOSTAR +20", BOTAO_VERDE, est["fichas_j"] > 0)
  else:
    rotulo_nova = (
        "REINICIAR TORNEIO"
        if (est["fichas_j"] <= 0 or est["fichas_b"] <= 0)
        else "PRÓXIMA MÃO"
    )
    desenhar_botao(btn_nova, rotulo_nova, BOTAO_AZUL, True)


def jogar():
  estado = iniciar_mao(500, 500)
  btn_fold = pygame.Rect(140, 540, 170, 46)
  btn_call = pygame.Rect(365, 540, 170, 46)
  btn_raise = pygame.Rect(590, 540, 170, 46)
  btn_nova = pygame.Rect(LARGURA // 2 - 120, 540, 240, 46)

  while True:
    for evento in pygame.event.get():
      if evento.type == pygame.QUIT:
        pygame.quit()
        sys.exit()

      if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
        pos = evento.pos
        if not estado["fim_rodada"]:
          if btn_fold.collidepoint(pos):
            estado["fichas_b"] += estado["pote"]
            estado["pote"] = 0
            estado["status"] = "Você desistiu. O Bot levou o pote."
            estado["fim_rodada"] = True
          elif btn_call.collidepoint(pos):
            turno_bot(estado, 0)
            if not estado["fim_rodada"]:
              estado["status"] = f"Fase: {estado['fase']} - Sua vez"
          elif btn_raise.collidepoint(pos) and estado["fichas_j"] > 0:
            valor = min(20, estado["fichas_j"])
            estado["fichas_j"] -= valor
            estado["pote"] += valor
            turno_bot(estado, valor)
            if not estado["fim_rodada"]:
              estado["status"] = f"Fase: {estado['fase']} - Sua vez"
        else:
          if btn_nova.collidepoint(pos):
            if estado["fichas_j"] <= 0 or estado["fichas_b"] <= 0:
              estado = iniciar_mao(500, 500)
            else:
              estado = iniciar_mao(estado["fichas_j"], estado["fichas_b"])

    desenhar_tela(estado, btn_fold, btn_call, btn_raise, btn_nova)
    pygame.display.flip()
    relogio.tick(60)


jogar()
