import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QHBoxLayout, QVBoxLayout, QWidget, QGridLayout
from PyQt5.QtCore import Qt
import getpass
import string

# Create the main window
class MainWindow(QMainWindow):
    def __init__(self, num_players):
        super().__init__()
        self.num_players = num_players
        self.player_names = []
        self.scores = []
        self.name_labels = []
        self.score_labels = []
        self.init_ui()

    # Initialize the GUI
    def init_ui(self):
        # Set the window title and size
        self.setWindowTitle("Score Keeper")
        self.setFixedSize(800, 600)

        # Create a widget to hold the player rectangles
        widget = QWidget()
        self.setCentralWidget(widget)

        # Create a layout to hold the player rectangles
        layout = QGridLayout()
        widget.setLayout(layout)

        # Create a rectangle for each player
        for i in range(self.num_players):
            # Generate a random color for the rectangle
            color = f"#{hash(str(i)) % 0xffffff:06x}"

            # Create the rectangle
            rect = QWidget()
            rect.setStyleSheet(f"background-color: black; border-radius: 10px;")
            layout.addWidget(rect, 0, i, 1, 1)

            # Add the player's name label
            name_label = QLabel("")
            name_label.setStyleSheet("font-weight: bold; font-size: 32px; color: white;")
            name_label.setAlignment(Qt.AlignCenter)
            layout.addWidget(name_label, 0, i, 1, 1)

            # Add the player's score label
            score_label = QLabel("0")
            score_label.setStyleSheet("font-size: 48px; color: black;")
            score_label.setAlignment(Qt.AlignCenter)
            layout.addWidget(score_label, 1, i, 1, 1)

            # Add the player's name and score labels to their respective lists
            self.name_labels.append(name_label)
            self.score_labels.append(score_label)
        
        self.activateWindow()
        self.raise_()

    def get_secret_numbers(self):
        secret_numbers = {}
        for i in range(self.num_players):
            player_secret_number = None
            while player_secret_number is None or player_secret_number < 0 or player_secret_number > self.num_players:
                try:
                    player_secret_number = int(getpass.getpass(f"Player {i+1} ({self.player_names[i]}), please enter a number between [1,{self.num_players}] and press ENTER: "))
                    if player_secret_number < 1 or player_secret_number > self.num_players:
                        print("Error: The number must be between 0 and", self.num_players)
                except ValueError:
                    print("Error: The input must be a numeric value.")
            secret_numbers[self.player_names[i]] = player_secret_number
        return secret_numbers

    def update_scores(self, secret_numbers):
        unique_numbers = [num for num in set(secret_numbers.values()) if list(secret_numbers.values()).count(num) == 1]
        for i in range(self.num_players):
            player_name = self.player_names[i]
            picked_number = secret_numbers[player_name]
            if picked_number in unique_numbers:
                self.scores[i] += picked_number
            else:
                self.scores[i] -= picked_number

            # Update the score label
            score_label = self.score_labels[i]
            score_label.setText(str(self.scores[i]))

        # Start the main loop
        self.show()

    def report_winner(self):
        highest_score = max(self.scores)
        winners = [self.player_names[i] for i, score in enumerate(self.scores) if score == highest_score]
        
        # Print the final scores
        print("\nFinal Scores:")
        for i in range(self.num_players):
            print(f"{self.player_names[i]}: {self.scores[i]}")
        
        # Check if there is a single winner or a tie
        if len(winners) > 1:
            print("\nIt's a tie between the following players:")
            for winner in winners:
                print(winner)
        else:
            print(f"\nThe winner is {winners[0]}!")

        # Close the application
        QApplication.quit()

    def report_round(self, secret_numbers):
        # Print the player names (column headers)
        print("\n{:<20}".format(''), end='')
        for player in self.player_names:
            print("{:<20}".format(player), end='')
        print()

        # Print the secret number choices
        print("{:<20}".format('Secret Numbers:'), end='')
        for player in self.player_names:
            print("{:<20}".format(secret_numbers[player]), end='')
        print()

        # Print the current scores
        print("{:<20}".format('Scores:'), end='')
        for i in range(self.num_players):
            print("{:<20}".format(self.scores[i]), end='')
        print()

def is_empty_or_whitespace(string):
    return not string or string.isspace()

def contains_punctuation(s):
    return any(c in string.punctuation for c in s)



if __name__ == "__main__":
    # Create the application
    app = QApplication(sys.argv)
    print('\n')
    print("WELCOME to Mert's Game, enjoy!")
    # Get the number of players from the user
    while True:
        try:    
            num_players = int(input("Enter the number of players: "))
            if num_players < 1:  # add some sanity check if needed
                print("Please enter a positive number!")
                continue
            break
        except ValueError:
            print("Invalid input. Please enter a number.")

    # Create the main window
    window = MainWindow(num_players)

    # Prompt the user to enter the name of each player
    for i in range(num_players):
        while True:
            name = input(f"Enter the name of player {i+1}: ")
            if not name.isdigit() and not is_empty_or_whitespace(name) and not contains_punctuation(name):
                break
            else:
                if name.isdigit():
                    print('The name cannot be solely numeric. Please enter a valid name. \n')
                elif is_empty_or_whitespace(name):
                    print('The name cannot be whitespace or empty. Please enter a valid name.\n')
                elif contains_punctuation(name):
                    print('The name cannot contain punctuations. Please enter a valid name.\n')
                else:
                    print('Please enter a valid name.\n')

        window.player_names.append(name)
        window.scores.append(0)

        # Update the name label
        name_label = window.name_labels[i]
        name_label.setText(name)

        # Update the score label
        score_label = window.score_labels[i]
        score_label.setText("0")


    # Get the number of rounds from the user
    print('\n')
    print('Recommended number of round is ', 2*num_players)
    print('\n') 
    while True:
        try:    
            num_rounds = int(input("Enter the number of rounds: "))
            if num_rounds < 1:  # add some sanity check if needed
                print("Please enter a positive number!")
                continue
            break
        except ValueError:
            print("Invalid input. Please enter a number.")


    # Play the game for the specified number of rounds
    for round in range(num_rounds):
        print(f"\nROUND {round + 1}:")
        secret_numbers = window.get_secret_numbers()
        window.update_scores(secret_numbers)
        window.report_round(secret_numbers)

    #report the winner
    window.report_winner()

    # Run the application
    sys.exit(app.exec_())
