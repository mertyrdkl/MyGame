import sys
import string
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QWidget, QGridLayout
from PyQt5.QtCore import Qt
import getpass

class InvalidPlayerInput(Exception):
    pass

class NameIsNumeric(Exception):
    pass

class NameIsEmpty(Exception):
    pass

class NameContainsPunctuation(Exception):
    pass

class Player:
    def __init__(self, name):
        self.name = name
        self.score = 0

    def __str__(self):
        return self.name


class MainWindow(QMainWindow):
    def __init__(self, players):
        super().__init__()
        self.players = players
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Score Keeper")
        self.setFixedSize(800, 600)

        widget = QWidget()
        self.setCentralWidget(widget)
        layout = QGridLayout()
        widget.setLayout(layout)

        for i, player in enumerate(self.players):
            color = f"#{hash(str(i)) % 0xffffff:06x}"
            rect = QWidget()
            rect.setStyleSheet(f"background-color: black; border-radius: 10px;")
            layout.addWidget(rect, 0, i, 1, 1)

            name_label = QLabel(player.name)
            name_label.setStyleSheet("font-weight: bold; font-size: 32px; color: white;")
            name_label.setAlignment(Qt.AlignCenter)
            layout.addWidget(name_label, 0, i, 1, 1)

            score_label = QLabel(str(player.score))
            score_label.setStyleSheet("font-size: 48px; color: black;")
            score_label.setAlignment(Qt.AlignCenter)
            layout.addWidget(score_label, 1, i, 1, 1)

            player.name_label = name_label
            player.score_label = score_label

        self.activateWindow()
        self.raise_()

    def get_secret_numbers(self):
        secret_numbers = {}
        for player in self.players:
            player_secret_number = None
            while player_secret_number is None or player_secret_number < 0 or player_secret_number > len(self.players):
                try:
                    player_secret_number = int(getpass.getpass(f"{player.name}, please enter a number between [1,{len(self.players)}] and press ENTER: "))
                    if player_secret_number < 1 or player_secret_number > len(self.players):
                        print("Error: The number must be between 1 and", len(self.players))
                except ValueError:
                    print("Error: The input must be a numeric value.")
            secret_numbers[player.name] = player_secret_number
        return secret_numbers

    def update_scores(self, secret_numbers):
        unique_numbers = [num for num in set(secret_numbers.values()) if list(secret_numbers.values()).count(num) == 1]
        for player in self.players:
            picked_number = secret_numbers[player.name]
            if picked_number in unique_numbers:
                player.score += picked_number
            else:
                player.score -= picked_number

            player.score_label.setText(str(player.score))

        self.show()

    def report_winner(self):
        highest_score = max([player.score for player in self.players])
        winners = [player.name for player in self.players if player.score == highest_score]

        print("\nFinal Scores:")
        for player in self.players:
            print(f"{player.name}: {player.score}")

        if len(winners) > 1:
            print("\nIt's a tie between the following players:")
            for winner in winners:
                print(winner)
        else:
            print(f"\nThe winner is {winners[0]}!")

        print('The game has ended.')
        QApplication.quit()

    def report_round(self, secret_numbers):
        print("\n{:<20}".format(''), end='')
        for player in self.players:
            print("{:<20}".format(player.name), end='')
        print()

        print("{:<20}".format('Secret Numbers:'), end='')
        for player in self.players:
            print("{:<20}".format(secret_numbers[player.name]), end='')
        print()

        print("{:<20}".format('Scores:'), end='')
        for player in self.players:
            print("{:<20}".format(player.score), end='')
        print()


def validate_player_name(name):
    if name.isdigit():
        raise NameIsNumeric
    if not name or name.isspace():
        raise NameIsEmpty
    if any(c in string.punctuation for c in name):
        raise NameContainsPunctuation
    return name


def validate_num_players(num_players):
    if num_players < 2:
        raise InvalidPlayerInput
    return num_players


if __name__ == "__main__":
    app = QApplication(sys.argv)
    print('\n')
    print("WELCOME to Mert's Game, enjoy!")

    while True:
        try:    
            num_players = validate_num_players(int(input("Enter the number of players: ")))
            break
        except ValueError:
            print("Invalid input. Please enter a number.")
        except InvalidPlayerInput:
            print("Invalid input. There must be at least 2 players.")

    players = []
    for i in range(num_players):
        while True:
            try:
                name = validate_player_name(input(f"Enter the name of player {i+1}: "))
                players.append(Player(name))
                break
            except NameIsNumeric:
                print('The name cannot be solely numeric. Please enter a valid name.\n')
            except NameIsEmpty:
                print('The name cannot be whitespace or empty. Please enter a valid name.\n')   
            except NameContainsPunctuation:
                print('The name cannot contain punctuations. Please enter a valid name.\n')
            

    window = MainWindow(players)

    print('\n')
    print('Recommended number of round is ', 2*num_players)
    print('\n') 
    while True:
        try:    
            num_rounds = int(input("Enter the number of rounds: "))
            if num_rounds < 1: 
                print("Please enter a positive number!")
                continue
            break
        except ValueError:
            print("Invalid input. Please enter a number.")

    for round in range(num_rounds):
        print(f"\nROUND {round + 1}:")
        secret_numbers = window.get_secret_numbers()
        window.update_scores(secret_numbers)
        window.report_round(secret_numbers)

    window.report_winner()

    sys.exit(app.exec_())
