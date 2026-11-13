# 📖 Tutorial: instalar e rodar os jogos no VS Code

Passo a passo para quem nunca configurou o ambiente. Siga na ordem. Os comandos de **Windows** e **Linux/macOS** aparecem separados quando são diferentes.

**Tempo estimado:** 20 a 30 minutos.

---

## Passo 1 — Instalar o Python

1. Acesse <https://www.python.org/downloads/> e baixe a versão mais recente (3.10 ou superior).
2. **Windows:** na primeira tela do instalador, marque a caixa **"Add python.exe to PATH"** *antes* de clicar em *Install Now*.
   **Linux (Ubuntu/Debian):**
   ```bash
   sudo apt update
   sudo apt install python3 python3-pip python3-venv
   ```
3. Confirme a instalação abrindo um terminal e digitando:
   ```bash
   python --version
   ```
   (No Linux/macOS, use `python3 --version`.) Deve aparecer algo como `Python 3.12.x`.

> ⚠️ Se no Windows aparecer "python não é reconhecido", tente `py --version`. Se também falhar, reinstale o Python marcando a opção do PATH.

---

## Passo 2 — Instalar o VS Code

1. Baixe em <https://code.visualstudio.com/> e instale.
2. Abra o VS Code.
3. Clique no ícone de **Extensões** (barra lateral esquerda, ou `Ctrl+Shift+X`).
4. Pesquise **Python** (autor: Microsoft) e clique em **Install**.
5. Instale também o **Pylance** se ele não vier junto.

---

## Passo 3 — Instalar o Git (opcional)

Só é necessário para clonar o repositório. Se preferir, pule para o **Passo 4 (opção B)**.

- **Windows:** baixe em <https://git-scm.com/download/win> e instale com as opções padrão.
- **Linux:** `sudo apt install git`

---

## Passo 4 — Obter o código

### Opção A: clonar com Git

1. No VS Code, abra o terminal: menu **Terminal → New Terminal** (atalho `` Ctrl+` ``).
2. Escolha uma pasta onde guardar o projeto e rode:
   ```bash
   git clone https://github.com/ArthurX10/etib.git
   ```

### Opção B: baixar o ZIP

1. Acesse <https://github.com/ArthurX10/etib>.
2. Clique no botão verde **Code → Download ZIP**.
3. Extraia o ZIP em uma pasta de sua preferência.

---

## Passo 5 — Abrir a pasta no VS Code

1. Menu **File → Open Folder…** (Arquivo → Abrir Pasta).
2. Selecione a pasta **`etib`** (a que contém `snake.py`, `Tetris.py` etc.).
3. Se o VS Code perguntar *"Do you trust the authors of the files in this folder?"*, clique em **Yes, I trust the authors**.

Você deve ver os arquivos `.py` na barra lateral esquerda (Explorer).

---

## Passo 6 — Criar o ambiente virtual

O ambiente virtual (**venv**) isola as bibliotecas do projeto, sem mexer no resto do computador. **Neste curso, os jogos sempre rodam dentro da venv**: o Pygame é instalado só nela.

No terminal do VS Code (**Terminal → New Terminal**), dentro da pasta `etib`:

**Windows (PowerShell):**
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

**Linux / macOS:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

Quando der certo, aparece **`(.venv)`** no início da linha do terminal.

Confirme que está dentro da venv:

```bash
python -c "import sys; print(sys.prefix != sys.base_prefix)"
```

Deve imprimir `True`.

> ⚠️ **Windows: erro "a execução de scripts foi desabilitada neste sistema"?**
> Rode uma vez: `Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned`, responda `S` e tente ativar de novo.
> Alternativa: troque o terminal para **Command Prompt** (seta ao lado do `+` no terminal) e use `.venv\Scripts\activate.bat`.

---

## Passo 7 — Instalar o Pygame

Com o ambiente ativado (`(.venv)` visível). **Não instale fora da venv**:

```bash
pip install -r requirements.txt
```

Para conferir:

```bash
python -c "import pygame; print(pygame.version.ver)"
```

Deve imprimir a versão (ex.: `2.6.1`).

---

## Passo 8 — Selecionar o interpretador no VS Code

Para o VS Code usar o Python do ambiente virtual:

1. Pressione `Ctrl+Shift+P` para abrir a **Paleta de Comandos**.
2. Digite **Python: Select Interpreter** e pressione Enter.
3. Escolha a opção que contém **`.venv`** (algo como `Python 3.12.x ('.venv')`).

No canto inferior direito da janela aparece o interpretador escolhido.

> 💡 O projeto já inclui a pasta `.vscode/`, que faz o terminal do VS Code **ativar a `.venv` automaticamente** sempre que um terminal novo é aberto. Ainda assim, confira o `(.venv)` no terminal e o interpretador no canto inferior direito.

---

## Passo 9 — Rodar um jogo

**Jeito 1: botão de play**

1. Clique em `snake.py` na barra lateral.
2. Clique no botão **▶ (Run Python File)** no canto superior direito do editor.

O botão usa o interpretador selecionado no Passo 8, ou seja, o da venv.

**Jeito 2: tecla F5 (com a configuração do projeto)**

1. Pressione `F5` (ou abra a aba **Run and Debug**, `Ctrl+Shift+D`).
2. Escolha um jogo na lista: **Snake**, **Breakout**, **Tetris**, **TopGear**, **Poker** ou **Arquivo atual**.

**Jeito 3: pelo terminal (com a venv ativa)**

```bash
python snake.py
```

Se preferir não depender da ativação, chame o Python da venv diretamente:

```bash
# Windows
.venv\Scripts\python.exe snake.py

# Linux / macOS
.venv/bin/python snake.py
```

Uma janela do jogo abrirá. Para sair, feche a janela.

Faça o mesmo com os outros jogos:

```bash
python Breakout.py
python Tetris.py
python TopGear.py
python Poker.py
```

### Controles

| Jogo | Controles |
|---|---|
| Snake | Setas ou WASD · **R**/**Espaço** reinicia |
| Breakout | Setas ou A/D · **R** reinicia |
| Tetris | ← → move · ↓ desce · ↑ gira · **Espaço** queda rápida · **R** reinicia |
| TopGear | ← → ou A/D · **R**/**Espaço** reinicia |
| Poker | Clique nos botões com o mouse |

---

## Passo 10 — Mexer no código (primeiro experimento)

1. Abra `snake.py`.
2. Procure (`Ctrl+F`) por `COBRA_CABECA = (45, 210, 110)` e troque por `(255, 100, 0)`.
3. Salve (`Ctrl+S`) e rode de novo. A cabeça da cobra mudou de cor. 🎉

Outras ideias rápidas:

- Em `snake.py`, mude `velocidade = 10` para `velocidade = 5` (mais lento).
- Em `Breakout.py`, mude `vidas = 3` para `vidas = 10`.
- Em `Tetris.py`, mude `velocidade = 500` para `velocidade = 150` (mais difícil).

Veja mais atividades na seção **Sugestões de atividades** do [README.md](README.md).

---

## Passo 11 (opcional) — Depurar com breakpoints

1. Clique à esquerda do número de uma linha para criar um ponto vermelho (*breakpoint*).
2. Pressione `F5` e escolha **Python File**.
3. O jogo pausa na linha marcada. Use `F10` para avançar linha a linha e veja os valores das variáveis no painel à esquerda.

---

## 🧯 Solução de problemas

| Problema | Causa provável | Solução |
|---|---|---|
| `ModuleNotFoundError: No module named 'pygame'` | O jogo está rodando **fora** da venv (venv desativada ou interpretador errado) | Ative o `.venv` (Passo 6), instale (Passo 7) e selecione o interpretador (Passo 8). Confira com `python -c "import sys; print(sys.prefix != sys.base_prefix)"`: deve dar `True`. |
| Botão ▶ roda, mas dá erro de pygame | O VS Code está usando outro interpretador | `Ctrl+Shift+P` → **Python: Select Interpreter** → escolha o `.venv`. Depois feche o terminal antigo e abra um novo. |
| `python` não reconhecido | Python fora do PATH | Use `py` (Windows) ou reinstale marcando *Add to PATH*. |
| `pip` não reconhecido | Mesmo motivo | Use `python -m pip install -r requirements.txt`. |
| Script de ativação bloqueado (Windows) | Política de execução do PowerShell | Veja a observação no Passo 6. |
| `error: externally-managed-environment` (Linux) | Tentou instalar fora do venv | Ative o `.venv` antes do `pip install`. |
| `No module named venv` (Linux) | Pacote ausente | `sudo apt install python3-venv`. |
| Janela não abre / erro de vídeo (WSL ou servidor) | Sem ambiente gráfico | Rode em Windows/Linux com interface gráfica; o WSL precisa do WSLg. |
| Letras ou naipes (♠ ♥) estranhos no Poker | Fonte Arial ausente | Troque `"arial"` por uma fonte disponível em `pygame.font.SysFont`. |
| Jogo lento | Computador muito limitado | Feche outros programas; reduza `LARGURA`/`ALTURA` no início do arquivo. |

---

## ✅ Checklist final

- [ ] Python instalado (`python --version`)
- [ ] VS Code com a extensão Python
- [ ] Pasta `etib` aberta no VS Code
- [ ] Ambiente virtual criado e ativado (`(.venv)` no terminal)
- [ ] Pygame instalado (`pip install -r requirements.txt`)
- [ ] Interpretador `.venv` selecionado
- [ ] `python -c "import sys; print(sys.prefix != sys.base_prefix)"` imprime `True`
- [ ] `snake.py` abriu a janela do jogo rodando pela venv

Se todos os itens estão marcados, você está pronto para o mini-curso! 🚀
