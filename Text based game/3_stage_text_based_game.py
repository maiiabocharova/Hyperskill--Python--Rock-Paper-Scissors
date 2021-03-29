class Game:
    def __init__(self):
        self.welcome = """***Welcome to the Journey to Mount Qaf***,
              1- Press key '1' or type 'start' to start a new game,
              2- Press key '2' or type 'load' to load your progress,
              3- Press key '3' or type 'quit' to quit the game"""
        self.mode = "menu"
        self.database = {}
        self.outcomes = {}
        with open("story/story.txt") as f:
            self.story = f.read().split('\n')
        with open("story/choices.txt") as f:
            self.choices = f.readlines()
        with open("story/outcomes.txt") as f:
            text = f.read().split("*")
            self.outcomes[0] = {1: text[0:3], 2: text[3:7], 3: text[7:10]}
            self.outcomes[1] = {1: text[10:13], 2: text[13:16], 3: text[16:20]}

    def main(self):
        if self.mode == "menu":
            self.main_menu()

    def main_menu(self):
        while True:
            print(self.welcome)
            selection = input().casefold()
            if selection == "1" or selection == "start":
                print("Starting a new game...")
                username = input("Enter a user name to save your progress or type '/b' to go back ")
                if username == '/b':
                    print("Going back to menu...\n")
                else:
                    self.create_new_user(username)
                    print("Good luck on your journey!")
                    print(f"Your character: {self.database[username]['name']}, {self.database[username]['species']}, {self.database[username]['gender']}")
                    print(f"Your inventory: {self.database[username]['snack']}, {self.database[username]['weapon']}, {self.database[username]['tool']}")
                    print(f"Difficulty: {self.database[username]['difficulty']}")
                    print()
                    self.play(username)
            elif selection == "2" or selection == "load":
                print("No save data found!")
            elif selection == "3" or selection == "quit":
                print("Goodbye!")
                quit()
            else:
                print("Unknown input! Please enter a valid one.")

    def create_new_user(self, username):
        print("Create your character:")
        self.database[username] = {'name': input("1- Name ").capitalize(),
                                   'species': input("2- Species ").capitalize(),
                                   'gender': input("3- Gender ").capitalize()}
        print("Pack your bag for the journey:")
        self.database[username].update({'snack': input("1- Favourite Snack ").capitalize(),
                                        'weapon': input("2- A weapon for the journey ").capitalize(),
                                        'tool': input("3- A traversal tool ").capitalize(),
                                        'key': False,
                                        'lives': 5,
                                        'level': 0, 'chapter': 0})
        while True:
            difficulty = input("Choose your difficulty:\n1- Easy\n2- Medium\n3- Hard\n").casefold()
            if difficulty == '1' or difficulty == 'easy':
                self.database[username]['difficulty'] = 'Easy'
                break
            elif difficulty == '2' or difficulty == 'medium':
                self.database[username]['difficulty'] = 'Medium'
                break
            elif difficulty == '3' or difficulty == 'hard':
                self.database[username]['difficulty'] = 'Hard'
                break
            print("Unknown input! Please enter a valid one.")

    def play(self, username):
        while True:
            if not self.database[username]['chapter']:  # Prints the level title if at chapter 0.
                print(self.story[self.database[username]['level'] * 4])
                self.database[username]['chapter'] += 1
            print(self.story[self.database[username]['level'] * 4 + self.database[username]['chapter']])
            self.make_choice(username)

    def make_choice(self, username):
        print("What will you do? Type the number of the option or type '/h' to show help.")
        print()
        for i in range(3):
            print(f"{i+1}- {self.choices[self.database[username]['level'] * 9 + (self.database[username]['chapter'] - 1) * 3 + i]}", end="")
        print()
        self.choice_outcome(username)

    def choice_outcome(self, username):
        while True:
            selection = input()
            if selection == "/i":
                print(f"Inventory: {self.database[username]['snack']}, {self.database[username]['weapon']}, {self.database[username]['tool']}")
                continue
            elif selection == "/q":
                if input("You sure you want to quit the game? Y/N").upper() == "Y":
                    print("Goodbye!")
                    quit()
            elif selection == "/c":
                print(f"Your character: {self.database[username]['name']}, {self.database[username]['species']}, {self.database[username]['gender']}.")
                print(f"Lives remaining: {self.database[username]['lives']}")
                continue
            elif selection == "/h":
                print("Type the number of the option you want to choose.",
                      "Commands you can use:",
                      "/i => Shows inventory.",
                      "/q => Exits the game.",
                      "/c => Shows the character traits.",
                      "/h => Shows help.", sep="\n")
                continue
            elif selection in ('1', '2', '3'):
                self.execute_event(username, int(selection))
                break
            else:
                print("Unknown input! Please enter a valid one.")
                continue

    def execute_event(self, username, choice):
        if self.database[username]['level'] == 0 and self.database[username]['chapter'] == 2:
            event_text = self.outcomes[0][2][0] if self.database[username]['key'] and choice == 1 else self.outcomes[0][2][choice]
        else:
            event_text = self.outcomes[self.database[username]['level']][self.database[username]['chapter']][choice-1].replace("{tool}", self.database[username]['tool'])

        print(event_text[:event_text.index(" (")])
        print()
        action_text = event_text[event_text.index("("):event_text.index(")")]

        if "inventory+'key'" in action_text:
            self.database[username]['key'] = True
        if "inventory-'key'" in action_text:
            self.database[username]['key'] = False

        if "life+1" in action_text:  # "life+1" also works as a "move".
            self.database[username]['lives'] += 1
            print("You gained an extra life! Lives remaining:", self.database[username]['lives'])
            self.advance_chapter(username)

        if "life-1" in action_text:  # Do something when lives = 0 ?
            self.database[username]['lives'] -= 1
            self.database[username]['chapter'] = 0
            print("You died! Lives remaining:", self.database[username]['lives'])
            print()

        if "move" in action_text:
            self.advance_chapter(username)

    def advance_chapter(self, username):
        self.database[username]['chapter'] += 1
        if self.database[username]['chapter'] > 3:
            self.database[username]['chapter'] = 0
            self.database[username]['level'] += 1
        if self.database[username]['level'] == 1:
            print("Level 2")
            print()
            print("Goodbye!")
            quit()

game = Game()
game.main()
© 2021 GitHub, Inc.
