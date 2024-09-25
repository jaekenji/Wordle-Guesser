# Wordle-Solver

[WORDLE](https://www.nytimes.com/games/wordle/index.html) solver that evaluates the best possible next guess based on entropy. The solver checks the current guess against the target word list using color-coded feedback.

After each guess, the solver eliminates words from the possible answers based on the feedback, calculates the entropy for each potential guess, and recommends the guess that will provide the most information.
