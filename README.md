# 🎮 Mini-curso de Jogos em Python com Pygame — ETIB / IFCE

Coleção de seis jogos clássicos feitos em **Python + Pygame**, usados como material prático do mini-curso do **ETIB – IFCE**. Cada jogo é um arquivo único e independente, pensado para ser lido, executado e modificado pelos alunos.

## 🕹️ Jogos

| Arquivo | Jogo | Conceitos que ele ensina | Controles |
|---|---|---|---|
| `snake.py` | Jogo da Cobrinha | listas, grade, loop de jogo, recorde | Setas ou **WASD** · **R** / **Espaço** reinicia |
| `Breakout.py` | Breakout | colisão de retângulos, vidas, ângulo da bola | Setas ou **A / D** · **R** reinicia |
| `Tetris.py` | Tetris | matrizes, rotação de peças, linhas completas, níveis | **← →** move · **↓** desce · **↑** gira · **Espaço** queda rápida · **R** reinicia |
| `TopGear.py` | Corrida pseudo-3D | projeção de perspectiva, dificuldade crescente | **← →** ou **A / D** troca de faixa · **R** / **Espaço** reinicia |
| `TennisForTwo.py` | Tennis for Two (1958) | física: gravidade, parábola, quique, trigonometria (ângulo → velocidade) | **J1:** W/S ângulo · D bate  ·  **J2:** ↑/↓ ângulo · ← bate · **G** guia · **R** reinicia |
| `Poker.py` | Texas Hold'em (você vs. bot) | dicionários, `Counter`, `itertools.combinations`, IA simples | **Mouse** (botões na tela) |

## ✅ Pré-requisitos

- **Python 3.10 ou superior** (testado com Python 3.12)
- **Pygame 2.1 ou superior** (usa `border_radius`, que só existe no Pygame 2)
- **Visual Studio Code** com a extensão *Python*
- **Git** (opcional, só para clonar; também dá para baixar o ZIP)

## 🚀 Início rápido

```bash
# 1. Clonar o repositório
git clone https://github.com/ArthurX10/etib.git
cd etib

# 2. Criar e ativar o ambiente virtual
python -m venv .venv
# Windows (PowerShell):  .venv\Scripts\Activate.ps1
# Linux / macOS:         source .venv/bin/activate

# 3. Instalar as dependências
pip install -r requirements.txt

# 4. Rodar um jogo
python snake.py
```

> No Linux/macOS, use `python3` no lugar de `python` (apenas no comando que **cria** a venv; depois de ativada, `python` funciona).

### ⚠️ Os jogos devem rodar dentro da venv

O Pygame é instalado **somente** na venv (`.venv`). Por isso, sempre execute os jogos com a venv ativa (você vê `(.venv)` no início da linha do terminal) ou chame o Python da venv diretamente:

```bash
# Windows
.venv\Scripts\python.exe snake.py

# Linux / macOS
.venv/bin/python snake.py
```

Para conferir se está dentro da venv:

```bash
python -c "import sys; print(sys.prefix != sys.base_prefix)"
```

Deve imprimir `True`. Se imprimir `False`, a venv não está ativa.

O projeto já traz a pasta `.vscode/` configurada: ao abrir a pasta no VS Code, o terminal ativa a `.venv` sozinho e o botão **▶** / `F5` usam o interpretador selecionado (veja o [TUTORIAL.md](TUTORIAL.md)).

📖 **Primeira vez com o VS Code?** Siga o passo a passo completo em [TUTORIAL.md](TUTORIAL.md).

## 📁 Estrutura do projeto

```
etib/
├── Breakout.py        # Jogo de quebrar blocos
├── Poker.py           # Texas Hold'em contra o bot
├── Tetris.py          # Tetris
├── TennisForTwo.py    # Tennis for Two (1958), 2 jogadores
├── TopGear.py         # Corrida em perspectiva
├── snake.py           # Jogo da cobrinha
├── requirements.txt   # Dependências (pygame)
├── .vscode/           # Configuração do VS Code (usa a .venv)
├── .gitignore         # Ignora a pasta .venv
├── README.md          # Este arquivo
└── TUTORIAL.md        # Instalação e execução no VS Code
```

## 🧠 Estrutura comum dos jogos

Todos seguem o mesmo esqueleto, o que ajuda a entender um e já saber ler os outros:

1. `pygame.init()` e criação da janela (`LARGURA`, `ALTURA`).
2. Constantes de **cores** e **fontes** no topo do arquivo.
3. Funções auxiliares (desenhar, colisão, gerar elementos).
4. Uma função `jogar()` com o **loop principal**: *eventos → lógica → desenho → `flip()` → `tick()`*.
5. Um laço final que chama `jogar()` de novo, permitindo reiniciar com **R**.

## 🧪 Sugestões de atividades

**Nível básico** (mudar valores e ver o resultado)
- `snake.py`: altere `velocidade` inicial, `TAMANHO_BLOCO` e as cores da cobra.
- `Breakout.py`: mude o número de `linhas`/`colunas` e as `CORES_BLOCOS`; aumente o número de `vidas`.
- `TopGear.py`: ajuste `intervalo_inimigos` e as cores de `CORES_INIMIGOS`.

**Nível intermediário** (acrescentar funcionalidades)
- Adicionar **pausa** com a tecla `P` em qualquer jogo.
- Salvar o **recorde** em um arquivo de texto para não perder ao fechar.
- `Snake`: criar paredes que "atravessam" a tela (aparece do outro lado).
- `Tetris`: mostrar a **próxima peça** (a variável `proxima_peca` já existe, falta desenhá-la).

**Sobre o Tennis for Two** (bom para uma aula de Física + Programação)
- Mude `GRAVIDADE` e veja a parábola mudar (tente simular a Lua: cerca de 1/6 da gravidade da Terra).
- Aperte **G** para ver a trajetória prevista e compare com a fórmula do alcance, `v² · sen(2θ) / g`: qual ângulo dá o maior alcance?
- Altere `REDE_ALTURA`, `COEF_QUICA` e `VELOCIDADE_BATIDA` e observe como o jogo fica mais fácil ou difícil.
- Desafio: criar um **bot** para o Jogador 2, escolhendo o ângulo que faz a bola cair perto do Jogador 1.

**Nível avançado** (desafios)
- `Breakout`: blocos que precisam de 2 batidas e *power-ups*.
- `Poker`: permitir valores de aposta variados e melhorar a decisão do bot em `turno_bot`.
- `TopGear`: adicionar curvas na pista alterando o `x` por fatia em `desenhar_estrada`.

## 🛠️ Problemas comuns

| Sintoma | Solução |
|---|---|
| `ModuleNotFoundError: No module named 'pygame'` | O jogo não está rodando na venv. Ative-a, rode `pip install -r requirements.txt` e confira se o VS Code usa o interpretador `.venv`. |
| `python` não é reconhecido (Windows) | Reinstale o Python marcando **Add Python to PATH** ou use `py` no lugar de `python`. |
| Janela abre e fecha na hora | Rode pelo terminal do VS Code para ver a mensagem de erro. |
| Símbolos de naipes (♠ ♥ ♦ ♣) não aparecem no Poker | A fonte Arial não está disponível no sistema; troque por outra em `pygame.font.SysFont`. |

Mais detalhes no [TUTORIAL.md](TUTORIAL.md).

## 📚 Referências

- [Documentação do Pygame](https://www.pygame.org/docs/)
- [Documentação do Python](https://docs.python.org/pt-br/3/)
- [Python no VS Code](https://code.visualstudio.com/docs/python/python-tutorial)

---

Material didático do mini-curso do **ETIB – IFCE**. Sinta-se livre para estudar, modificar e compartilhar com os colegas.
