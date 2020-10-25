import random, sqlite3

menu1 = """1. Create an account
2. Log into account
0. Exit
"""
suc_log = """1. Balance
2. Add income
3. Do transfer
4. Close account
5. Log out
0. Exit
"""
CREATE_ACC = "CREATE TABLE IF NOT EXISTS card (id INTEGER PRIMARY KEY, number TEXT, pin TEXT, balance INTEGER DEFAULT 0);"
INSERT_ACC = "INSERT INTO card (number, pin) VALUES (?, ?);"
GET_PIN = "SELECT pin FROM card WHERE number = ?;"
GET_BALANCE = "SELECT balance FROM card WHERE number = ?;"
ADD_INCOME = "UPDATE card SET balance = balance + ? WHERE number = ?;"
CLOSE_ACC = "DELETE FROM card WHERE number = ?;"
WITHDRAW = "UPDATE card SET balance = balance - ? WHERE number = ?;"
DROP = "DELETE FROM card"
connection = sqlite3.connect('card.s3db')
def clean(connection):
    with connection:
        connection.execute(DROP)
clean(connection)
def create_acc(connection):
    with connection:
        connection.execute(CREATE_ACC)
def add_acc(connection, number, pin):
    with connection:
        connection.execute(INSERT_ACC, (number, pin))
def get_pin(connection, number):
    with connection:
        return connection.execute(GET_PIN, (number,)).fetchone()
def get_balance(connection, number):
    with connection:
        return connection.execute(GET_BALANCE, (number,)).fetchone()
def add_income(connection, money, number):
    with connection:
        connection.execute(ADD_INCOME, (money, number))
def withdraw(connection, money, number):
    with connection:
        connection.execute(WITHDRAW, (money, number))
def close_acc(connection, number):
    with connection:
        connection.execute(CLOSE_ACC, (number,))

def create():
    a = random.randint(000000000,999999999)
    random.seed(0)
    b = list(map(int, str(a)))
    for i in b[::2]:
        b[b.index(i)]=i*2
    for j in b:
        if j > 9:
            b[b.index(j)] = j-9
    d = 10-(8 + sum(b))%10
    if d == 10:
        d = 0
    num = int("400000" + str(a) + str(d))
    print(f"Your card has been created\nYour card number:\n{num}")
    pin = random.randint(0000, 9999)
    print(f"Your card PIN:\n{pin}")
    random.seed(0)
    add_acc(connection, num, pin)
    main()
def check(trans_card):
    def digits_of(n):
        return [int(d) for d in str(n)]
    digits = digits_of(trans_card)
    odd_digits = digits[-1::-2]
    even_digits = digits[-2::-2]
    checksum = 0
    checksum += sum(odd_digits)
    for d in even_digits:
        checksum += sum(digits_of(d*2))
    return (checksum % 10 == 0)
def logged(number):
    choice = int(input(suc_log))
    if choice == 1:
        print(f"Balance: {get_balance(connection, number)[0]}")
        logged(number)
    if choice == 2:
        money = int(input("Enter income:\n"))
        add_income(connection, money, number)
        print("Income was added!")
        logged(number)
    if choice == 3:
        print("Transfer")
        trans_card = int(input("Enter card number:\n"))
        if check(trans_card):
            if trans_card == number:
                print("You can't transfer money to the same account!")
                logged(number)
            if not get_pin(connection, trans_card):
                print("Such a card does not exist.")
                logged(number)
            else:
                money = int(input("Enter how much money you want to transfer:\n"))
                if money>get_balance(connection, number)[0]:
                    print("Not enough money!")
                    logged(number)
                else:
                    add_income(connection, money, trans_card)
                    withdraw(connection, money, number)
                    print("Success!")
                    logged(number)
        else:
            print("Probably you made a mistake in the card number. Please try again!")
            logged(number)
    if choice == 4:
        close_acc(connection, number)
        print("The account has been closed!")
        main()
    if choice == 0:
        print("Bye!")
def log_in():
    number = int(input("Enter your card number:"))
    pin_en = input("Enter your PIN:")
    result = get_pin(connection, number)
    if result:
        if get_pin(connection, number)[0] != pin_en:
            print("Wrong card number or PIN!")
            main()
        else:
            print("You have successfully logged in!")
            logged(number)
    else:
        print("Wrong card number or PIN!")
        main()
def main():
    create_acc(connection)
    choice = int(input(menu1))
    if choice == 1:
        create()
    if choice == 2:
        log_in()
    if choice == 0:
        print("Bye!")
main()
