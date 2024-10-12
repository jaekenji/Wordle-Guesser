import math

banner = """
best start word: SALET
"""

class Wordle:
    def __init__(self, guesses, answers) -> None:
        self.guesses         = guesses
        self.answers         = answers
        self.guess           = ""
        self.pattern         = ""
        self.best_guess      = "salet"
        self.running         = True

    def start(self) -> None:
        while self.running:
            self.guesser()

    def guesser(self) -> None:
        self.guess           = input("guess: ").lower()
        self.pattern         = input("colors: ").lower()

        if not self.guess or not self.pattern:
            self.running     = False
            return

        if self.guess not in self.guesses:
            print("word isnt guessable!")
            return

        self.checker()

        if not self.answers:
            self.running     = False
            return

        self.next_guess()

        print(self.best_guess)

        if len(self.answers) == 1:
            self.running     = False
            return
    
    def checker(self) -> None:
        good_letters         = [letter for index, letter in enumerate(self.guess) if self.pattern[index] != "b"]

        for index, letter in enumerate(self.guess):
            if self.pattern[index] == "g":
                self.answers = [word for word in self.answers if letter == word[index]]
            if self.pattern[index] == "y":
                self.answers = [word for word in self.answers if letter != word[index] and letter in word]
            if self.pattern[index] == "b" and letter not in good_letters:
                self.answers = [word for word in self.answers if letter not in word]

    def next_guess(self) -> None:
        if len(self.answers) < 3:
            self.best_guess  = self.answers[0]
            return

        best_word            = ""
        best_entropy         = 0

        for guess in self.guesses:
            entropy          = self.entropy(guess)
            if entropy > best_entropy:
                best_word    = guess
                best_entropy = entropy

        self.best_guess = best_word

    def entropy(self, guess) -> float:
        patterns             = {}

        for answer in self.answers:
            pattern          = self.get_pattern(guess, answer)
            patterns[pattern] = patterns.get(pattern, 0) + 1

        total_answers        = len(self.answers)
        entropy              = self.calculate_entropy(patterns, total_answers)
        return entropy

    def get_pattern(self, guess, answer) -> str:
        pattern              = [""] * 5

        for index, letter in enumerate(guess):
            if letter == answer[index]:
                pattern[index] = "g"
            if letter != answer[index] and letter in answer:
                pattern[index] = "y"
            if letter not in answer:
                pattern[index] = "b"

        pattern = "".join(pattern)
        return pattern

    def calculate_entropy(self, patterns, total_answers) -> float:
        entropies            = []

        for pattern, count in patterns.items():
            probility        = count / total_answers
            entropy_amount   = math.log2(1 / probility)
            entropies       += [entropy_amount] * count

        entropy              = sum(entropies) / len(entropies)
        return entropy

def main() -> None:
    guesses                  = open("guesses.txt", "r").read().split("\n")
    answers                  = open("answers.txt", "r").read().split("\n")

    print(banner)

    while True:
        wordle               = Wordle(guesses, answers)
        wordle.start()

        if not input("type anything to continue . . ."):
            break

if __name__ == "__main__":
    main()