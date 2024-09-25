import customtkinter as ctk
import math

guesses = open("guesses.txt","r").read().split("\n")
answers = open("answers.txt","r").read().split("\n")

class Wordle:
    def __init__(self):
        self.app                     = None
        self.squares_frame           = None
        self.squares_and_labels      = {}
        self.square_row_now          = 0
        self.square_now              = 0
        self.square_colors           = {
            "#79B851": "#F3C237", 
            "#F3C237": "#292929", 
            "#292929": "#79B851"
        }
        self.best_word_frame         = None
        self.best_word_label         = None

        # actual wordle logic
        self.possible_guesses        = guesses
        self.possible_answers        = answers
        self.best_word               = "slate"

        self.start()   

    # starts the gui portion
    def start(self):
        if not self.initialize():
            print("[!] Failed to configure app.")

        if not self.build_restart():
            print("[!] Failed to build restart button.")

        if not self.build_squares_frame():
            print("[!] Failed to build squares' frame.")

        if not self.build_squares():
            print("[!] Failed to build squares.")

        if not self.build_best_frame():
            print("[!] Failed to build best word frame.")

        if not self.build_best_label():
            print("[!] Failed to build best word label.")
        
        self.app.mainloop()

    def restart(self):
        self.square_row_now          = 0
        self.square_now              = 0

        for row in range(6):
            for column in range(5):
                square, label        = self.squares_and_labels[(row, column)]
                square.configure(
                    fg_color         = "#101010",
                    border_color     = "#252525"
                )
                label.configure(
                    text             = ""
                )

        self.possible_answers        = answers
        self.possible_guesses        = guesses
        self.best_word               = "slate"
        self.update_best_word()


    # makes a dark app and sets up a key press event (handmade typing text box)
    def initialize(self):
        self.app                     = ctk.CTk()
        self.app.geometry(
            "500x665"
        )
        self.app.title(
            "Wordle"
        )
        self.app.resizable(
            False, 
            False
        )
        self.app.configure(
            fg_color                 = "#101010"
        )
        self.app.bind(
            "<KeyPress>", 
            self.key_clicked
        )
        return True
    
    # build restart button
    def build_restart(self):
        restart_button               = ctk.CTkButton(
            self.app,
            width                    = 120,
            height                   = 30,
            text                     = "Restart", 
            command                  = self.restart, 
            fg_color                 = "#79B851", 
            text_color               = "#F0F0F0", 
            hover_color              = "#6CA44A",
            font                     = ("Shoika Medium", 16)
        )
        restart_button.place(
            relx                     = 0.5,
            y                        = 50,
            anchor                   = "n"
        )
        return True

    # builds a frame to hold all guessing blocks
    def build_squares_frame(self):
        self.squares_frame           = ctk.CTkFrame(
            self.app, 
            width                    = 340, 
            height                   = 410, 
            fg_color                 = "#101010",
            bg_color                 = "#101010",
            border_width             = 0
        )
        self.squares_frame.place(
            x                        = 80,
            y                        = 120
        )
        return True

    # builds the squares (guessing blocks)
    def build_squares(self):
        for row in range(6):
            for column in range(5):
                square               = self.create_square(row, column)
                label                = self.create_label(square)
                self.squares_and_labels[(row, column)] = (square, label)
        return True

    # creates a square at a given location
    def create_square(self, row, col):
        square                       = ctk.CTkFrame(
            self.squares_frame, 
            width                    = 60,
            height                   = 60, 
            corner_radius            = 10, 
            fg_color                 = "#101010",
            border_color             = "#252525",
            border_width             = 2
        )
        square.place(
            x                        = col * 70,
            y                        = row * 70
        )                         
        return square             
            
    # creates a label for a given square
    def create_label(self, square):
        square_label                 = ctk.CTkLabel(
            square,               
            text                     = "", 
            font                     = ("Shoika Bold", 30), 
            text_color               = "#F0F0F0"
        )
        square_label.place(
            relx                     = 0.5,
            rely                     = 0.5,
            anchor                   = "center"
        )
        return square_label

    # build frame for best word
    def build_best_frame(self):
        self.best_word_frame         = ctk.CTkFrame(
            self.app, 
            width                    = 300, 
            height                   = 100, 
            corner_radius            = 20,
            fg_color                 = "#0D0D0D",
            bg_color                 = "#101010",
            border_width             = 0
        )
        self.best_word_frame.place(
            relx                     = 0.5,
            y                        = 550,
            anchor                   = "n"
        )
        return True
    
    # build label for best word
    def build_best_label(self):
        self.best_word_label         = ctk.CTkLabel(
            self.best_word_frame, 
            text                     = self.best_word.upper(), 
            font                     = ("Shoika Bold", 32), 
            text_color               = "#F0F0F0"
        )
        self.best_word_label.place(
            relx                     = 0.5, 
            rely                     = 0.5, 
            anchor                   = "center"
        )
        return True

    # update best word (fancy)
    def update_best_word(self):
        self.fade_out()
        return True

    # begin fading out
    def fade_out(self, step=100):
        if step >= 0:
            intensity                = int(240 * (step / 100))
            step                     = f"#{intensity:02x}{intensity:02x}{intensity:02x}"
            self.best_word_label.configure(
                text_color           = step)
            self.app.after(
                10, 
                self.fade_out, 
                step - 5
            )
        else:
            self.best_word_label.configure(
                text                 = self.best_word.upper()
            )
            self.fade_in()

    # begin fading in
    def fade_in(self, step=0):
        if step <= 100:
            intensity                = int(240 * (step / 100))
            step                     = f"#{intensity:02x}{intensity:02x}{intensity:02x}"
            self.best_word_label.configure(
                text_color           = step
            )
            self.app.after(
                10,
                self.fade_in,
                step + 5
            )

    # handle key presses
    def key_clicked(self, event):
        key = event.char.upper()

        if key in "ABCDEFGHIJKLMNOPQRSTUVWXYZ" and event.char.isalpha() and self.square_now < 5:
            self.type_letter(key)

        if event.keysym == "BackSpace":
            self.delete_letter()

        if event.keysym == "space":
            self.change_color()

        if event.keysym == "Return" and self.square_now == 5:
            word                     = self.verify_word()
            if not word:
                return
            
            colors                   = self.verify_color()
            if not colors:
                return
            
            self.do_wordle(word, colors)
            self.square_row_now     += 1
            self.square_now          = 0

    # set letter to label at given square
    def type_letter(self, letter):
        square                       = self.squares_and_labels[(self.square_row_now, self.square_now)][0]
        square.configure(
            border_color             = "#707070"
        )
        square_label                 = self.squares_and_labels[(self.square_row_now, self.square_now)][1]
        square_label.configure(
            text                     = letter
        )
        self.square_now             += 1

    # remove letter to a label at given square
    def delete_letter(self):
        if self.square_now == 0:
            return

        self.square_now             -= 1
        square                       = self.squares_and_labels[(self.square_row_now, self.square_now)][0]
        square.configure(
            fg_color                 = "#101010",
            border_color             = "#252525"
        )
        square_label                 = self.squares_and_labels[(self.square_row_now, self.square_now)][1]
        square_label.configure(
            text                     = ""
        )

    # updates the guessed color for current square
    def change_color(self):
        if self.square_now == 0:
            return

        square                       = self.squares_and_labels[(self.square_row_now, self.square_now - 1)][0]
        current_color                = square.cget("fg_color")

        if current_color not in self.square_colors:
            next_color               = "#79B851"
        else:
            next_color               = self.square_colors[current_color]

        square.configure(
            fg_color                 = next_color,
            border_color             = next_color,
        )

    # wordle logic
    
    # gets the inputted word-
    def verify_word(self):
        word_now                     = ""
        for square in range(5):
            label                    = self.squares_and_labels[(self.square_row_now, square)][1]
            letter                   = label.cget("text").lower()
            word_now                += letter

        if word_now not in self.possible_guesses:
            return

        return word_now

    # gets the colors to the inputted word
    def verify_color(self):
        colors                       = []
        for square in range(5):
            frame                    = self.squares_and_labels[(self.square_row_now, square)][0]
            color                    = frame.cget("fg_color")
            if color == "#101010":
                return

            colors.append(color)

        return colors

    # break down list and send off guess
    def do_wordle(self, word, hex_colors):
        color_map                    = {
            "#79B851": "G",
            "#F3C237": "Y",
            "#292929": "B"
        }
        colors                       = ""
        for hex_color in hex_colors:
            color                    = color_map[hex_color]
            colors                  += color

        self.green_checker(word, colors)
        self.yellow_checker(word, colors)
        self.gray_checker(word, colors)

        self.best_word               = self.next_guess()
        self.update_best_word()

        return True

    # reduces list based on greens / yellows / grays
    def green_checker(self, guess, pattern):
        green_format                 = [guess[index] + str(index) for index in range(5) if pattern[index] == "G"]
        for green_char in green_format:
            letter                   = green_char[0]
            place                    = int(green_char[1])
            self.possible_answers    = [word for word in self.possible_answers if word[place] == letter]

    def yellow_checker(self, guess, pattern):
        # updated solution for dupes
        green_places                 = [index for index in range(5) if pattern[index] == "G"]
        yellow_places                = [index for index in range(5) if pattern[index] == "Y"]

        yellow_format                = [(guess[index], index) for index in yellow_places]
    
        duplicates_included          = self.possible_answers
        for letter, yellow_place in yellow_format:
            # craziest line here - all words possible if: letter is in the word and not in the spot guessed, and if there are duplicates make sure they are not in the green spots as well 
            duplicates_included = [word for word in duplicates_included if letter in word and word[yellow_place] != letter and sum(1 for i, c in enumerate(word) if c == letter and i not in green_places) >= len(yellow_places)]
        
        self.possible_answers = duplicates_included

    def gray_checker(self, guess, pattern):
        good_letters                 = [guess[index] for index in range(5) if pattern[index] != "B"]
        # protect any letters that are good
        gray_letters                 = [guess[index] for index in range(5) if pattern[index] == "B" and guess[index] not in good_letters]
        for gray_char in gray_letters:
            self.possible_answers    = [word for word in self.possible_answers if gray_char not in word]

    # go through all possible guesses and send back the most informative
    def next_guess(self):
        best_guess                   = None
        best_entropy                 = -float('inf')

        for guess in self.possible_guesses:
            entropy                  = self.get_best_entropy(guess)
            if entropy > best_entropy:
                best_entropy         = entropy
                best_guess           = guess

        if len(self.possible_answers) <= 2:
            best_guess               = self.possible_answers[0]

        return best_guess

    # take all patterns with their occurrences and send for calculation
    def get_best_entropy(self, guess):
        pattern_count                = {}

        for answer in self.possible_answers:
            pattern                  = self.get_pattern(guess, answer)
            if pattern in pattern_count:
                pattern_count[pattern] += 1
            else:
                pattern_count[pattern] = 1

        total_answers                = len(self.possible_answers)
        entropy                      = self.calculate_entropy(pattern_count, total_answers)
        return entropy

    # retrieves a pattern based on the correct word vs every possible guess 
    def get_pattern(self, guess, target):
        pattern                      = ["", "", "", "", ""]
        target_list                  = list(target)

        self.mark_greens(guess, pattern, target_list)
        self.mark_yellows(guess, pattern, target_list)
        self.mark_grays(guess, pattern, target_list)

        pattern                      = "".join(pattern)
        return pattern

    # quickly create a green / yellow /gray marking
    def mark_greens(self, guess, pattern, targets):
        for index, letter in enumerate(guess):
            if letter == targets[index]:
                pattern[index]       = "G"
                targets[index]       = None

    def mark_yellows(self, guess, pattern, targets):
        for index, letter in enumerate(guess):
            if pattern[index] == "":
                if letter in targets:
                    pattern[index]   = "Y"
                    targets[targets.index(letter)] = None

    def mark_grays(self, guess, pattern, targets):
        for index, letter in enumerate(guess):
            if pattern[index] == "":
                if letter not in targets:
                    pattern[index]   = "B"
    
    # use shannon entropy to find total entropy of patterns and their counts
    def calculate_entropy(self, pattern_count, total_count):
        entropy = 0
        for count in pattern_count.values():
            probability              = count / total_count
            if probability > 0:
                entropy_amount       = probability * math.log2(probability)
                entropy             -= entropy_amount

        return entropy

if __name__ == "__main__":
    Wordle()
