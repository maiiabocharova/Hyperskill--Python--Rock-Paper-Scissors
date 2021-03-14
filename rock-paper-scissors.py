import random

name = input('Enter your name: ')
print(f'Hello, {name}')
score = 0

with open('rating.txt') as file:
    for line in file:
        player_name, player_score = line.split()
        if name == player_name:
            score = int(player_score)
            break

options = input().split(',')
if options == ['']:
    options = ['rock', 'paper', 'scissors']
print("Okay, let's start")

while True:
    player = input()
    if player == '!exit':
        print('Bye')
        break
    if player == '!rating':
        print(f'Your rating: {score}')
        continue
    if player not in options:
        print('Invalid input')
        continue
    computer = random.choice(options)
    if computer == player:
        score += 50
        print(f'There is a draw ({computer})')
    else:
        offset = (options.index(computer) - options.index(player)) % len(options)
        if offset > len(options) // 2:
            score += 100
            print(f'Well done. Computer chose {computer} and failed')
        else:
            print(f'Sorry, but computer chose {computer}')
