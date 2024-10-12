import pygame
import math

class Wordle:
    def __init__(self, guesses, answers):
        self.wordle_game                = pygame
        self.main_display               = self.wordle_game.display
        self.game_clock                 = self.wordle_game.time.Clock()
        self.font                       = None

        self.squares_and_pos            = [""] * 30
        self.square_row_now             = 0
        self.square_now                 = 0
        self.square_colors              = {
            "#79B851": "#F3C237", 
            "#F3C237": "#292929", 
            "#292929": "#79B851"
        }

        self.letters                    = {}
        self.possible_guesses           = guesses
        self.possible_answers           = answers
        self.animation_graph            = [(1, 70), (2, 65), (3, 62), (4, 61), (5, 60)]

        self.running                    = True

    def start(self):
        self.initialize()
        self.start_run()

    def initialize(self):
        self.wordle_game.init()
        self.screen                     = self.main_display.set_mode((500, 665))
        self.main_display.set_caption("Wordle")
        self.font                       = self.wordle_game.font.Font(None, 48)
        self.build_squares()
        self.draw_squares()

    def build_squares(self):
        possible_postions               = [(row, col) for row in range(6) for col in range(5)]
        for position in possible_postions:
            index                       = possible_postions.index(position)

            row                         = position[0]
            col                         = position[1]
            x                           = 80  + col * 70
            y                           = 127 + row * 70

            square                      = self.wordle_game.Rect(x, y, 60, 60)
            stroke_color                = "#252525"
            fill_color                  = "#101010"

            self.squares_and_pos[index] = (row, col), square, stroke_color, fill_color
            self.letters[(row, col)]    = ""

    def start_run(self):
        while self.running:
            self.update_game()

    def update_game(self):
        event_object                    = self.wordle_game.event.get()
        animation_type                  = None
        if not event_object:
            return

        event = event_object[0]
        if event.type == self.wordle_game.WINDOWCLOSE:
            self.running = False

        if event.type == self.wordle_game.KEYDOWN:
            animation_type              = self.handle_key_press(event.unicode)

        if animation_type:
            self.pop_squares()

        self.screen.fill("#101010")
        self.draw_squares()
        self.game_clock.tick(60)
        self.main_display.update()

    def draw_squares(self):
        for (row, col), square, stroke_color, fill_color in self.squares_and_pos:
            self.wordle_game.draw.rect(
                self.screen,
                fill_color,
                square
            )
            self.wordle_game.draw.rect(
                self.screen, 
                stroke_color, 
                square, 
                2
            )
            letter                      = self.letters[(row, col)]
            paint_letter                = self.font.render(
                letter, 
                True, 
                "#F0F0F0"
            )
            letter_in_square            = paint_letter.get_rect(
                center                  = square.center
            )
            self.screen.blit(paint_letter, letter_in_square)

    def pop_squares(self):
        square_now                      = (self.square_row_now * 5) + self.square_now - 1
        (row, col), square, stroke_color, fill_color = self.squares_and_pos[square_now]

        exact_x_pos                     = square[0]
        exact_y_pos                     = square[1]

        for frame, scale in self.animation_graph:
            new_x_pos                   = exact_x_pos - ((scale - 60) / 2)
            new_y_pos                   = exact_y_pos - ((scale - 60) / 2)
            new_square                  = self.wordle_game.Rect(new_x_pos, new_y_pos, scale, scale)

            self.squares_and_pos[square_now] = (row, col), new_square, stroke_color, fill_color

            self.screen.fill("#101010")
            self.draw_squares()
            self.game_clock.tick(60)
            self.main_display.update()

        self.squares_and_pos[square_now] = (row, col), square, stroke_color, fill_color

    def handle_key_press(self, character):
        if character.isalpha():
            self.handle_letter(character.upper())
            return 1

        if character.encode() == b"\x08":
            self.handle_backspace()

        if character == " ":
            self.handle_space()

        if character.encode() == b"\r":
            self.handle_enter()

    def handle_letter(self, letter):
        row                             = self.square_row_now
        col                             = self.square_now

        if row > 5:
            return

        if col > 4:
            return

        self.letters[(row, col)]        = letter
        self.highlight_letter()
        self.square_now                += 1

    def highlight_letter(self):
        square_now                      = (self.square_row_now * 5) + self.square_now
        pos, square, stroke, fill       = self.squares_and_pos[square_now]
        self.squares_and_pos[square_now] = pos, square, "#707070", "#101010"

    def handle_backspace(self):
        if self.square_now == 0:
            return

        self.square_now                -= 1
        row                             = self.square_row_now
        col                             = self.square_now

        self.letters[(row, col)]        = ""
        self.delight_letter()

    def delight_letter(self):
        square_now                      = (self.square_row_now * 5) + self.square_now
        pos, square, stroke, fill       = self.squares_and_pos[square_now]
        self.squares_and_pos[square_now] = pos, square, "#252525", "#101010"

    def handle_space(self):
        if self.square_now == 0 or self.square_now > 5:
            return

        pos, square, stroke, fill       = self.squares_and_pos[(self.square_row_now * 5) + self.square_now - 1]

        if fill not in self.square_colors:
            fill                        = "#292929"
    
        stroke                          = self.square_colors[fill]
        fill                            = self.square_colors[fill]

        self.squares_and_pos[(self.square_row_now * 5) + self.square_now - 1] = (pos, square, stroke, fill)

    def handle_enter(self):
        first_color                     = self.square_row_now * 5 + self.square_now - 5
        final_color                     = self.square_row_now * 5 + self.square_now
        colors                          = [square_info[3] for square_info in self.squares_and_pos[first_color:final_color]]
        color_map                       = {
            "#79B851": "G", 
            "#F3C237": "Y", 
            "#292929": "B"
        }
        colors                          = [color_map[fill_color] for fill_color in colors if fill_color != "#101010"]
        colors                          = "".join(colors)
        
        if len(colors) != 5:   
            return

        letters                         = [self.letters[(self.square_row_now, index)].lower() for index in range(5)]
        word                            = "".join(letters)

        if word.lower() not in self.possible_guesses:
            return

        self.square_row_now            += 1
        self.square_now                 = 0
        self.do_wordle(word, colors)

    def do_wordle(self, word, colors):
        if len(self.possible_answers) == 0:
            return

        self.green_checker(word, colors)
        self.yellow_checker(word, colors)
        self.gray_checker(word, colors)

        new                             = self.next_guess()
        print(new)
        print(self.possible_answers)
        return True

    def green_checker(self, guess, pattern):
        green_format                    = [guess[index] + str(index) for index in range(5) if pattern[index] == "G"]
        for green_char in green_format:
            letter                      = green_char[0]
            place                       = int(green_char[1])
            self.possible_answers       = [word for word in self.possible_answers if word[place] == letter]

    def yellow_checker(self, guess, pattern):
        yellow_format                   = [guess[index] + str(index) for index in range(5) if pattern[index] == "Y"]
        for yellow_char in yellow_format:
            letter                      = yellow_char[0]
            place                       = int(yellow_char[1])
            self.possible_answers       = [word for word in self.possible_answers if letter in word and word[place] != letter]

    def gray_checker(self, guess, pattern):
        good_letters                    = [guess[index] for index in range(5) if pattern[index] != "B"]
        gray_letters                    = [guess[index] for index in range(5) if pattern[index] == "B" and guess[index] not in good_letters]
        for gray_char in gray_letters:
            self.possible_answers       = [word for word in self.possible_answers if gray_char not in word]

    def next_guess(self):
        best_guess                      = None
        best_entropy                    = 0

        for guess in self.possible_guesses:
            entropy                     = self.get_best_entropy(guess)
            if entropy > best_entropy:
                best_entropy            = entropy
                best_guess              = guess

        if len(self.possible_answers) <= 2:
            best_guess                  = self.possible_answers[0]

        return best_guess

    def get_best_entropy(self, guess):
        pattern_count                   = {}

        for answer in self.possible_answers:
            pattern                     = self.get_pattern(guess, answer)
            if pattern in pattern_count:
                pattern_count[pattern] += 1
            else:
                pattern_count[pattern]  = 1

        total_answers                   = len(self.possible_answers)
        entropy                         = self.calculate_entropy(pattern_count, total_answers)
        return entropy

    def get_pattern(self, guess, target):
        pattern                         = [""] * 5

        for index, letter in enumerate(guess):
            if letter == target[index]:
                pattern[index]          = "g"

        for index, letter in enumerate(guess):
            if pattern[index] == "":
                if letter in target:
                    pattern[index]      = "y"
                else:
                    pattern[index]      = "b"

        pattern                         = "".join(pattern)
        return pattern        
        
    
    def calculate_entropy(self, pattern_count, total_count):
        entropies = []
        for count in pattern_count.values():
            probability                 = count / total_count
            entropy_amount              = math.log2(1 / probability)
            entropies                  += [entropy_amount] * count

        entropy = sum(entropies) / len(entropies)
        return entropy
            
if __name__ == "__main__":
    guess                               = open("guesses.txt","r").read().split("\n")
    answer                              = open("guesses.txt","r").read().split("\n")

    wordle                              = Wordle(guess, answer)
    wordle.start()
