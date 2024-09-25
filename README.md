# Wordle-Guesser

[WORDLE](https://www.nytimes.com/games/wordle/index.html) guesser that evaluates the best possible next guess based on probability and entropy. The solver checks all guesses, and finds the best word to reduce the most information.

After each guess, the solver eliminates words from the possible answers based on the feedback, calculates the entropy for each potential guess, and recommends the guess that will provide the most information.

![image](https://github.com/user-attachments/assets/eae45147-181d-4284-8404-50cd43ee35e7)

## How it works

For a given possible answers list, the solver goes through each potential guess, and evaluates that word. The word is sent with the possible pattern, and all patterns for all words are counted.

Once all guesses are counter, the probability is caluclated, and ran through the shannon entropy to give a bit value to the new information.
