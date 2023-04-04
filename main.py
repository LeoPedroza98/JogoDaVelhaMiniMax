import random


def getBoardCopy(board):
  dupeBoard = []

  for i in board:
    dupeBoard.append(i)
  return dupeBoard


def PrintBoard(board):
  copyBoard = getBoardCopy(board)

  for i in range(1, 10):
    if (board[i] == ''):
      copyBoard[i] = str(i)
    else:
      copyBoard[i] = board[i]

  print(' ' + copyBoard[7] + '|' + copyBoard[8] + '|' + copyBoard[9])
  print('-------')
  print(' ' + copyBoard[4] + '|' + copyBoard[5] + '|' + copyBoard[6])
  print('-------')
  print(' ' + copyBoard[1] + '|' + copyBoard[2] + '|' + copyBoard[3])
  print('-------')


def input_player():
  while True:
    letter = input('Você quer ser X ou O? ').upper()
    if letter not in ('X', 'O'):
      print('Digite apenas a letra X ou O.')
    else:
      break

  if letter == 'X':
    return ['X', 'O']
  else:
    return ['O', 'X']


def primeiroJogador():
  if random.randint(0, 1) == 0:
    return 'computador'
  else:
    return 'jogador'


def movimento(board, letter, move):
  board[move] = letter


def souGanhador(brd, let):
  return ((brd[7] == let and brd[8] == let and brd[9] == let)
          or (brd[4] == let and brd[5] == let and brd[6] == let)
          or (brd[1] == let and brd[2] == let and brd[3] == let)
          or (brd[7] == let and brd[4] == let and brd[1] == let)
          or (brd[8] == let and brd[5] == let and brd[2] == let)
          or (brd[9] == let and brd[6] == let and brd[3] == let)
          or (brd[7] == let and brd[5] == let and brd[3] == let)
          or (brd[9] == let and brd[5] == let and brd[1] == let))


def espacoVazio(board, move):
  if (board[move] == ''):
    return True
  else:
    return False


def get_move(board):
  while True:
    move = input('Qual é o seu próximo movimento? (1-9) ')
    if move.isdigit() and int(move) in range(1, 10) and espacoVazio(
        board, int(move)):
      break
    else:
      if not move.isdigit():
        print('ERRO: Insira um número entre 1 e 9.')
      elif int(move) not in range(1, 10):
        print('ERRO: Insira um número entre 1 e 9.')
      elif not espacoVazio(board, int(move)):
        print(
          'ERRO: O espaço escolhido já está ocupado. Escolha outro espaço.')
  return int(move)


def RandomMovimento(board, movesList):
  possiveisMovimentos = []
  for i in movesList:
    if espacoVazio(board, i):
      possiveisMovimentos.append(i)

  if len(possiveisMovimentos) != 0:
    return random.choice(possiveisMovimentos)
  else:
    return None


def BoardSemEspaco(board):
  for i in range(1, 10):
    if espacoVazio(board, i):
      return False
  return True


def possiveisOpcoes(board):

  opcoes = []

  for i in range(1, 10):
    if espacoVazio(board, i):
      opcoes.append(i)

  return opcoes


def JogoDaVelha(board, computerLetter):
  if computerLetter == 'X':
    playerLetter = 'O'
  else:
    playerLetter = 'X'

  if (souGanhador(board, computerLetter)):
    return 1

  elif (souGanhador(board, playerLetter)):
    return -1

  elif (BoardSemEspaco(board)):
    return 0

  else:
    return None


def alphabeta(board, computerLetter, turn, alpha, beta):
  if computerLetter == 'X':
    playerLetter = 'O'
  else:
    playerLetter = 'X'

  if turn == computerLetter:
    nextTurn = playerLetter
  else:
    nextTurn = computerLetter

  finish = JogoDaVelha(board, computerLetter)

  if (finish != None):
    return finish

  possiveis = possiveisOpcoes(board)

  if turn == computerLetter:
    for move in possiveis:
      movimento(board, turn, move)
      val = alphabeta(board, computerLetter, nextTurn, alpha, beta)
      movimento(board, '', move)
      if val > alpha:
        alpha = val

      if alpha >= beta:
        return alpha
    return alpha

  else:
    for move in possiveis:
      movimento(board, turn, move)
      val = alphabeta(board, computerLetter, nextTurn, alpha, beta)
      movimento(board, '', move)
      if val < beta:
        beta = val

      if alpha >= beta:
        return beta
    return beta


def getComputerMove(board, turn, computerLetter):
  a = -2
  opcoes = []

  if computerLetter == 'X':
    playerLetter = 'O'
  else:
    playerLetter = 'X'

  for i in range(1, 10):
    copy = getBoardCopy(board)
    if espacoVazio(copy, i):
      movimento(copy, computerLetter, i)
      if souGanhador(copy, computerLetter):
        return i

  for i in range(1, 10):
    copy = getBoardCopy(board)
    if espacoVazio(copy, i):
      movimento(copy, playerLetter, i)
      if souGanhador(copy, playerLetter):
        return i

  possiveisOpcoesOn = possiveisOpcoes(board)

  for move in possiveisOpcoesOn:

    movimento(board, computerLetter, move)
    val = alphabeta(board, computerLetter, playerLetter, -2, 2)
    movimento(board, '', move)

    if val > a:
      a = val
      opcoes = [move]

    elif val == a:
      opcoes.append(move)

  return random.choice(opcoes)


print('--- MiniMax Jogo da Velha ---')

jogar = True

while jogar:
  board = [''] * 10
  playerLetter, computerLetter = input_player()
  turn = primeiroJogador()
  print('O ' + turn + ' joga primeiro,')
  game = True

  while game:
    if turn == 'jogador':
      PrintBoard(board)
      move = get_move(board)
      movimento(board, playerLetter, move)

      if souGanhador(board, playerLetter):
        PrintBoard(board)
        print('Woooow! Voce venceu o jogo!')
        game = False

      else:
        if BoardSemEspaco(board):
          PrintBoard(board)
          print('DEU VELHA,BOM JOGO!!')
          break
        else:
          turn = 'computador'

    else:
      move = getComputerMove(board, playerLetter, computerLetter)
      movimento(board, computerLetter, move)

      if souGanhador(board, computerLetter):
        PrintBoard(board)
        print("O computador venceu :(")
        game = False

      else:
        if BoardSemEspaco(board):
          PrintBoard(board)
          print('O jogo terminou empatado')
          break
        else:
          turn = 'jogador'

  letterNew = ''
while True:
  letterNew = input(
    "Você quer jogar novamente? Digite S (para sim) ou N (para não): ").strip(
    ).upper()
  if letterNew == 'S':
    break
  elif letterNew == 'N':
    print("Foi bom jogar com você! Até mais!")
    jogar = False
    break
  else:
    print("Entrada inválida! Digite S (para sim) ou N (para não)!")
