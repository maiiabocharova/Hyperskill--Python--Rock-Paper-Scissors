coffee_types = {
    1: {'water': 250, 'milk': 0, 'beans': 16, 'price': 4},
    2: {'water': 350, 'milk': 75, 'beans': 20, 'price': 7},
    3: {'water': 200, 'milk': 100, 'beans': 12, 'price': 6}
}
water_available = 400
milk_available = 540
beans_available = 120
cups_available = 9
money_available = 550
def remaining():
    print(f'The coffee machine has:')
    print(f'{water_available} of water')
    print(f'{milk_available} of milk')
    print(f'{beans_available} of coffee beans')
    print(f'{cups_available} of disposable cups')
    print(f'{money_available} of money')
def buy():
    global water_available, milk_available, beans_available, cups_available, money_available
    try:
        drink = int(input('What do you want to buy? 1 - espresso, 2 - latte, 3 - cappuccino:'))
        if coffee_types[drink]['water'] > water_available:
            print('Sorry, not enough water!')

        elif coffee_types[drink]['milk'] > milk_available:
            print('Sorry, not enough milk!')
        elif coffee_types[drink]['beans'] > beans_available:
            print('Sorry, not enough beans!')
        elif cups_available < 1:
            print('Sorry, not enough cups!')
        else:
            print('I have enough resources, making you a coffee!')
            water_available -= coffee_types[drink]['water']
            milk_available -= coffee_types[drink]['milk']
            beans_available -= coffee_types[drink]['beans']
            cups_available -= 1
            money_available += coffee_types[drink]['price']
    except:
        print('You should write 1,2,3')

def fill():
    global water_available, milk_available, beans_available, cups_available, money_available
    water = int(input('Write how many ml of water do you want to add:'))
    water_available += water
    milk = int(input('Write how many ml of milk do you want to add:'))
    milk_available += milk
    beans = int(input('Write how many grams of coffee beans do you want to add:'))
    beans_available += beans
    cups = int(input('Write how many cups of coffee you will need:'))
    cups_available += cups
choice = input('Write action (buy, fill, take, reamining, exit):')
while choice != 'exit':
    if choice == 'take':
        print(f'I gave you ${money_available}')
        money_available = 0
    elif choice == 'fill':
        fill()
    elif choice == 'buy':
        buy()
    elif choice == 'remaining':
        remaining()
    choice = input('Write action (buy, fill, take, reamining, exit):')
