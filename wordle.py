from collections import Counter

# --- Load Word Lists ---
try:
    with open('wordle-list.txt', 'r') as file:
        wordleanswers = file.read().splitlines()

    with open('wordle_possibles.txt', 'r') as file:
        wordleguesses = file.read().splitlines()
except FileNotFoundError:
    print("Error: Make sure 'wordle-list.txt' and 'wordle_possibles.txt' are in the same directory.")
    exit()

# --- Global State ---
correctspot = [' ', ' ', ' ', ' ', ' ']
inword = Counter() 
remainingwords = []
tempremaining = []
removedletters = set()
notinposition = [set(), set(), set(), set(), set()] 

# --- Statistics ---
answerlen = len(wordleanswers)
wordlescorrect = 0
firstcorrect = 0
secondcorrect = 0
thirdcorrect = 0
fourthcorrect = 0
fifthcorrect = 0
sixthcorrect = 0

def process_clues(guess, answer):
    """
    Processes a guess against an answer and updates the global state
    (correctspot, inword, removedletters, notinposition)
    with the new clues, correctly handling duplicate letters.
    """
    global inword, correctspot, removedletters, notinposition
    
    answer_counts = Counter(answer)
    guess_clues = ['_'] * 5
    
    # 1. Green Pass: Find all correct letters in the correct spot
    for i in range(5):
        if guess[i] == answer[i]:
            guess_clues[i] = 'G'
            correctspot[i] = guess[i]
            answer_counts[guess[i]] -= 1
            
    # 2. Yellow/Gray Pass: Find yellows and grays
    for i in range(5):
        if guess_clues[i] == '_':
            char = guess[i]
            if answer_counts[char] > 0:
                guess_clues[i] = 'Y'
                notinposition[i].add(char)
                answer_counts[char] -= 1
            else:
                guess_clues[i] = 'B'
                
    # 3. Update global knowledge from the clues
    current_guess_counts = Counter()
    for i in range(5):
        char = guess[i]
        if guess_clues[i] == 'G' or guess_clues[i] == 'Y':
            current_guess_counts[char] += 1
            
    # Update minimum required counts
    for char, count in current_guess_counts.items():
        inword[char] = max(inword[char], count)
        
    # Update pure grays (letters that are *only* gray)
    for i in range(5):
        char = guess[i]
        # If a letter is gray AND it's not required (i.e., not green/yellow)
        if guess_clues[i] == 'B' and inword[char] == 0:
            removedletters.add(char)

def filterguesses():
    """
    Filters the list of remaining possible answers based on the
    cumulative clues stored in the global state variables.
    """
    global remainingwords, tempremaining
    tempremaining.clear()
    
    list_to_filter = wordleanswers if not remainingwords else remainingwords
    
    for word in list_to_filter:
        valid = True
        word_counts = Counter(word)

        # 1. Green letters: Must be in the correct spot
        for i, c in enumerate(correctspot):
            if c != ' ' and word[i] != c:
                valid = False
                break
        if not valid: continue

        # 2. Yellow letters: Must not be in a known "wrong" spot
        for i, chars_set in enumerate(notinposition):
            if word[i] in chars_set:
                valid = False
                break
        if not valid: continue

        # 3. Minimum letter counts: Must have at least the known count
        for char, count in inword.items():
            if word_counts[char] < count:
                valid = False
                break
        if not valid: continue

        # 4. Gray letters: Must not contain any "pure gray" letters
        for char in removedletters:
            if word_counts[char] > 0:
                valid = False
                break
        if not valid: continue
        
        tempremaining.append(word)

    remainingwords.clear()
    remainingwords.extend(tempremaining)

def filternextguess():
    """
    Chooses the best guess by first checking 'remainingwords' (answers)
    and then checking 'wordleguesses' (non-answers) to find a
    word with an even better score.
    """
    # This safety check IS required because filtering can fail
    if len(remainingwords) == 0:
        return None # Return None to signal a failure
        
    if len(remainingwords) == 1:
        return remainingwords[0]

    if len(remainingwords) == 3:
        return remainingwords[0]

    letter_freq = Counter("".join(remainingwords))
    best_score = -1
    best_word = remainingwords[0]

    for word in remainingwords:
        score = sum(letter_freq[c] for c in set(word))
        if score > best_score:
            best_score = score
            best_word = word

    for word in wordleguesses:
        score = sum(letter_freq[c] for c in set(word))
        if score > best_score:
            best_score = score
            best_word = word 
    return best_word

def solve(answer):
    """
    Main solver loop for a single Wordle answer.
    """
    global wordlescorrect, firstcorrect, secondcorrect, thirdcorrect, fourthcorrect, fifthcorrect, sixthcorrect
    
    # Reset state for this word
    global inword, correctspot, remainingwords, tempremaining, removedletters, notinposition
    inword = Counter()
    correctspot = [' ', ' ', ' ', ' ', ' ']
    remainingwords = []
    tempremaining = []
    removedletters = set()
    notinposition = [set(), set(), set(), set(), set()]
    
    guesses = []
    
    for guess_num in range(1, 7): 
        
        # 1. Choose a guess
        if guess_num == 1:
            guess = "salet"
        else:
            guess = filternextguess()
            
        if not guess:
            print(f"Solver failed (no words left) for: {answer}. Guesses: {guesses}")
            return
            
        guesses.append(guess)
        
        # 2. Check if we won
        if guess == answer:
            wordlescorrect += 1
            if guess_num == 1: firstcorrect += 1
            elif guess_num == 2: secondcorrect += 1
            elif guess_num == 3: thirdcorrect += 1
            elif guess_num == 4: fourthcorrect += 1
            elif guess_num == 5: fifthcorrect += 1
            elif guess_num == 6: sixthcorrect += 1
            return
        
        # 3. Process the clues from the guess
        process_clues(guess, answer)
        
        # 4. Filter the word list
        filterguesses()
        
        # 5. Remove the guess itself 
        if guess in remainingwords:
            remainingwords.remove(guess)
            
    # If the loop finishes, we failed to guess in 6 tries
    print(f"Couldn't guess word in 6 tries. Answer was: {answer}. Guesses: {guesses}")


# --- RUN THE SOLVER ---
print(f"Starting solver for {answerlen} words...")

for word in wordleanswers:
    solve(word) 


# --- Calculations ---
print("--- RESULTS ---")
print(f"Total wordles correct: {wordlescorrect} / {answerlen}")
if answerlen > 0:
    print(f"Accuracy: {(wordlescorrect / answerlen) * 100:.2f} %")
if wordlescorrect > 0:
    sumofguess = (firstcorrect * 1 + secondcorrect * 2 + thirdcorrect * 3 +
                  fourthcorrect * 4 + fifthcorrect * 5 + sixthcorrect * 6)
    print(f"Average attempts to guess Wordle: {(sumofguess / wordlescorrect):.3f}")

print("\n--- Guess Distribution ---")
print(f"1 guess:  {firstcorrect}")
print(f"2 guesses: {secondcorrect}")
print(f"3 guesses: {thirdcorrect}")
print(f"4 guesses: {fourthcorrect}")
print(f"5 guesses: {fifthcorrect}")
print(f"6 guesses: {sixthcorrect}")
