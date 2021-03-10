import random
import itertools
from collections import Counter

class Domino:
    def __init__(self):
        self.cards = ([[a, b] for a in range(0, 7) for b in range(a, 7)])
        random.shuffle(self.cards)
        self.computer_pieces = []
        self.player_pieces = []
        self.snake = []
        self.status = ''
        self.end = False

    def shuffle(self):
        random.shuffle(self.cards)

    def choice(self):
        card = random.choice(self.cards)
        self.cards.remove(card)
        return card

    def form_pieces(self):
        double_domino = [-1, -1]
        for _ in range(7):
            computer_card = self.choice()
            player_card = self.choice()
            now_cards = [computer_card, player_card]
            for card in now_cards:
                if (card[0] == card[1]) and (card[0] > double_domino[0]):
                    double_domino = card
            self.computer_pieces.append(computer_card)
            self.player_pieces.append(player_card)
        if double_domino == [-1, -1]:
            self.cards += self.computer_pieces
            self.cards += self.player_pieces
            self.shuffle()
            return self.form_pieces()
        else:
            self.snake.append(double_domino)
            self.status = "player" if double_domino in self.computer_pieces else "computer"
            if double_domino in self.computer_pieces:
                self.computer_pieces.remove(double_domino)
            else:
                self.player_pieces.remove(double_domino)
    def print_computer(self):
        print(f'Computer pieces: {len(self.computer_pieces)}')

    def print_player(self):
        print('Your pieces:')
        for i, player_piece in enumerate(self.player_pieces):
            print(f'{i+1}:{player_piece}')

    def print_snake(self):
        if len(self.snake) <= 6:
            print(*self.snake)
        else:
            print(*self.snake[:3], end = '...')
            print(*self.snake[-3:])

    def print_stock(self):
        print(f'Stock size: {len(self.cards)}')

    def print_status(self):
        if self.status == 'player':
            print("Status: It's your turn to make a move. Enter your command.")
        else:
            print("Status: Computer is about to make a move. Press Enter to continue...")
            input()

    def make_move(self):
        if self.status == 'player':
            player_input = input()
            try:
                if int(player_input) == 0 and len(self.cards) != 0:
                    card = self.choice()
                    self.player_pieces.append(card)
                elif int(player_input) == 0 and len(self.cards) == 0:
                    pass
                elif int(player_input) < 0:
                    card = self.player_pieces[abs(int(player_input))-1]
                    if card[1] == self.snake[0][0]:
                        self.snake = [card] + self.snake
                        self.player_pieces.remove(card)
                    elif card[0] == self.snake[0][0]:
                        self.snake = [[card[1],card[0]]] + self.snake
                        self.player_pieces.remove(card)
                    else:
                        print('Illegal move. Please try again.')
                        self.make_move()
                else:
                    card = self.player_pieces[abs(int(player_input))-1]
                    if card[0] == self.snake[-1][1]:
                        self.snake.append(card)
                        self.player_pieces.remove(card)
                    elif card[1] == self.snake[-1][1]:
                        self.snake.append([card[1], card[0]])
                        self.player_pieces.remove(card)
                    else:
                        print('Illegal move. Please try again.')
                        self.make_move()
                self.status = 'computer'
            except:
                print('Invalid input. Please try again.')
                self.make_move()

        else:
            flat_snake = list(itertools.chain(*self.snake))
            comp_pieces = list(itertools.chain(*self.computer_pieces))
            available_pieces = flat_snake + comp_pieces
            cnt = Counter(available_pieces)
            rank_dominoes = {}
            for card in self.computer_pieces:
                rank_dominoes[tuple(card)] = cnt[card[0]] + cnt[card[1]]
            rank_dominoes = dict(sorted(rank_dominoes.items(), key=lambda item: item[1], reverse=True))
            checker = 0
            for card in rank_dominoes:
                card = list(card)
                if card[0] == self.snake[0][0]:
                    self.computer_pieces.remove(card)
                    self.snake = [[card[1],card[0]]] + self.snake
                    checker = 1
                    break
                elif card[1] == self.snake[0][0]:
                    self.computer_pieces.remove(card)
                    self.snake = [card] + self.snake
                    checker = 1
                    break
                elif card[0] == self.snake[-1][1]:
                    self.computer_pieces.remove(card)
                    self.snake.append(card)
                    checker = 1
                    break
                elif card[1] == self.snake[-1][1]:
                    self.computer_pieces.remove(card)
                    self.snake.append([card[1],card[0]])
                    checker = 1
                    break
            if checker == 0 and len(self.cards) != 0:
                card = self.choice()
                self.computer_pieces.append(card)
            elif checker == 0 and len(self.cards) == 0:
                pass
            self.status = 'player'

    def check(self):
        flat_snake = list(itertools.chain(*self.snake))
        if len(self.computer_pieces) == 0:
            self.end = True
            self.print_end()
            print('Status: The game is over. The computer won!')
            return False
        elif len(self.player_pieces) == 0:
            self.end = True
            self.print_end()
            print('Status: The game is over. You won!')
            return False
        elif flat_snake.count(flat_snake[0]) == 8:
            self.end = True
            self.print_end()
            print("Status: The game is over. It's a draw!")
            return False
        else:
            return True
    def print_end(self):
        print('======================================================================')
        self.print_stock()
        self.print_computer()
        self.print_snake()
        self.print_player()


def main():
    game = Domino()
    game.form_pieces()
    while not game.end:
        print('======================================================================')
        game.print_stock()
        game.print_computer()
        game.print_snake()
        game.print_player()
        game.print_status()
        game.make_move()
        game.check()


main()
