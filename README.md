# Wordle-Solver

[WORDLE](https://www.nytimes.com/games/wordle/index.html) solver that evaluates the best possible next guess based on entropy. The solver checks the current guess against the target word list using color-coded feedback (green for correct position, yellow for present but incorrect position, and gray for absent). After each guess, the solver eliminates words from the possible answers based on the feedback, calculates the entropy for each potential guess, and recommends the guess that will provide the most information, thereby narrowing down the solution efficiently.
