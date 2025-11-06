**Wordle Solver**

**Preamble**/n
This wordle solver successfully solves all 2315 valid wordle answers, using a combination of allowed guesses and answers. I had completed this project once before, over a year and a half ago and am pleased to exceed my expectations of myself.

**Statistics**/n
--- RESULTS ---/n
Total wordles correct: 2315 / 2315/n
Accuracy: 100.00 %/n
Average attempts to guess Wordle: 3.764/n

--- Guess Distribution ---/n
1 guess:  0/n
2 guesses: 3/n
3 guesses: 925/n
4 guesses: 1053/n
5 guesses: 284/n
6 guesses: 50/n

**Algorithm Used**/n
The structure of this solver was quite straight forward, guesses were filtered via a 'best guess score' which simply checked all possible answers or guesses to try and chose the word with the best score related to the current information we know.

**Issues**/n
At the end of my initial implementation I was stuck with 10 words that could not be completed. This was due to patterns in the words that had too many combinations of answers. For example, vaunt, taunt, haunt, jaunt. In order to combat these guesses, 
I used conditional checks on certain guesses to guess a word that would remove possible combinations, for 'aunt' ending words, I used the word "dight" to remove as many possible combinations of the first letter as possible. I ran a script on remaining words that had this issue to resolve all Wordle traps.

**Future modifications**/n
Future modifications will include reducing average guess time, either via a different sorting algorithm or more thorough checks.
