import random
import time
import os
import sys


#CHEATSHEET
#themedict = {"CHEMISTRYLAB":0, "BEAKER":1, "PIPETTE":2, "FLASK":3, 
             # "GOGGLES":4, "THERMOMETER":5}

#MEDICALCAREER:0, DENTIST:1, PHARMACIST:2, SURGEON:3, DOCTOR:4, 
#NURSE:5

#OFFICESUPPLIES:0, RULER:1, SCISSORS:2, STAPLER:3, PRINTER:4, PENCILS:5



themewords = {} 
hintwords = []
foundhintwords = []
themes = [] #STORE THEME WORDS FOUND
keys = []   #COOR
hints = 0 
hintsused = 0
themewordsfound = 0
lives = 10
found_words = set() #Used set to avoid duplicates

letters = [] #FOR THE BOARD
foundvalue = []
hintmessage = f"\tAccess a hint ({hints}/3)"
theme = ""
mode = ""


def load(mode):
    global theme
    
    os.system("clear && printf '\\e[3J'")
    with open(mode) as file:
        for i, line in enumerate(file):
            if i == 0:
                theme = line
                # print(f"\033[1;32mTheme: {line}", end="")
                print("\n")
                
            elif i in range(1,9):
                rowletter = []
                for letter in line.rstrip():
                    rowletter.append(letter)
                letters.append(rowletter)
            elif i in range(9, 17):
                row = []
                for n in line.rstrip():
                    row.append(int(n))
                keys.append(row)
            elif i in range(24,43):
                hintwords.append(line.rstrip())
            elif i in range(18,24):
                themewords[line.rstrip()] = i-18


def reset_game_state():
    #resets all variables and data structures to their initial state. 
    #used when player quits in the middle of the game or when the player wants to play again 
    global lives, mode, hintwords, foundhintwords, themewords, theme, keys, hints, themes, found_words, foundvalue, themewordsfound, hintsused
    mode = ""
    lives = 10
    hintwords.clear()
    foundhintwords.clear()
    themewords.clear()  
    theme = ""
    keys.clear()
    letters.clear()
    themes.clear()
    found_words.clear()
    foundvalue.clear()
    hints = 0
    themewordsfound = 0
    hintsused = 0


def highlight(value):  # Highlight theme words or hint words
    coordinates = []  
    # Loop through each row and column in keys to find all occurrences of `value`
    for rowIdx, row in enumerate(keys):
        for colIdx, colValue in enumerate(row):
            if colValue == value:
                # Append the (row, col) position to coordinates
                coordinates.append([rowIdx, colIdx])

    # Apply highlighting for the given value
    if value == 0:  
        for (row, col) in coordinates:
            letter = letters[row][col]
            # Skip if already highlighted
            if not letter.startswith("\033"):
                # print("SKIPPED")
                # time.sleep(1)
                # print(value)
                letters[row][col] = f"\033[1;33m[{letter}]\033[0m"
                
    else:       
        for (row, col) in coordinates:
            letter = letters[row][col]
            # Skip if already highlighted
            if not letter.startswith("\033"):
                # print("SKIPPED")
                # time.sleep(1)
                # print(value)
                letters[row][col] = f"\033[1;32m[{letter}]\033[1;37m"
                

def reset_highlighting():
    for rowIdx, row in enumerate(keys):
        for colIdx, colValue in enumerate(row):
            letters[rowIdx][colIdx] = letters[rowIdx][colIdx]


def highlighthint(value, highlight=True):
    coordinates = []
    for rowIdx, row in enumerate(keys):
        for colIdx, colValue in enumerate(row):
            if colValue == value:
                coordinates.append((rowIdx, colIdx))

    # Update each position in letters based on `highlight` mode
    for row, col in coordinates:
        letter = letters[row][col]
        if highlight:
            letters[row][col] = f"\033[1;33m({letter})"  # Highlight with parentheses
        else:
            letters[row][col] = letter.replace(f"\033[1;33m(", "").replace(")", "")  # Remove parentheses


def setupboard(puzzle, lives):
    print(f"\033[1;33mLives left: {lives}/10\n")
    print(f"\033[1;32m\tTheme: {theme}")

    for let in puzzle:

        for l in let:
            print(f"\033[1;37m{l}\t", end="")

        print("\n")



def userlogin(theme, hintsused, elapsedtime):
    username = input("Enter name: ")
   
    with open(theme, 'a') as ldb:
        ldb.write(f"{username},")
        ldb.write(f"{str(hintsused)},")
        ldb.write(f"{str(elapsedtime)}\n")

        
def typewritereffect(text, delay=0.01):
    for char in text:
        # print(char)
        sys.stdout.write(char)
        # sys.stdout.flush()
        time.sleep(delay)
    print()

def play(hints,themewordsfound, hintmessage, hintsused, lives):
    starttime = time.time()

    while True:
        # print("\033[?25l", end="", flush=True)

        word = input("Enter a word: ").upper()

        if word in themewords.keys() and word not in found_words and lives > 0:
            
            os.system("clear && printf '\\e[3J'") #clear the screen once the game starts
            value = themewords[word]
            
            foundvalue.append(themewords[word])
            found_words.add(word)
            themes.append(word)
            highlighthint(value, highlight=False)
            highlight(value)
            setupboard(letters, lives)

            themewordsfound += 1
            if value == 0:  
                for key, value1 in themewords.items():
                    if value1 == value:
                        print(f"\033[1;33m\tSPANGRAM! {key}\033[1;37m") 
            
            print(f"\tTheme word found! {word}")                        
            if hints == 3:
                hintmessage = "\tHINT AVAILABLE [Type 'hint' and press enter]"
                print(hintmessage)
            else:
                print(f"\tAccess a hint ({hints}/3)")
            print(f"Hint words found: {' '.join(foundhintwords)}")
            print(f"Theme words found: ({themewordsfound}/6): {' '.join(themes)}") #using join method to avoid using for loop
            

            if themewordsfound == 6:

                os.system("clear && printf '\\e[3J'")
                elapsedtime = round(time.time() - starttime, 2)
                congrats = """\033[1;33m

\t ██████╗ ██████╗ ███╗   ██╗ ██████╗ ██████╗  █████╗ ████████╗███████╗██╗
\t██╔════╝██╔═══██╗████╗  ██║██╔════╝ ██╔══██╗██╔══██╗╚══██╔══╝██╔════╝██║
\t██║     ██║   ██║██╔██╗ ██║██║  ███╗██████╔╝███████║   ██║   ███████╗██║
\t██║     ██║   ██║██║╚██╗██║██║   ██║██╔══██╗██╔══██║   ██║   ╚════██║╚═╝
\t╚██████╗╚██████╔╝██║ ╚████║╚██████╔╝██║  ██║██║  ██║   ██║   ███████║██╗
\t ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝   ╚══════╝╚═╝                                                                                    
\033[1;37m"""

                typewritereffect(congrats, delay=0.005)
                print("You found all the theme words.")
                userlogin(theme.strip(), hintsused, elapsedtime)
                
                os.system("clear && printf '\\e[3J'")
                
                setupboard(letters, lives)
                
                
                print(f"\tTheme word found! {word}")
                print(f"\tAccess a hint ({hints}/3)")
                print(f"Theme words found: ({themewordsfound}/6): {' '.join(themes)}") #using join method to avoid using for loop
                print(f"Hint words found: {' '.join(foundhintwords)}")
                print("All theme words found. Congratulations!")
            
                print("\tAccess high scores [Type 'hs' and press enter]")
                print("\tQuit game [Type 'q' and press enter]")
                print(f"Elapsed time: {round(elapsedtime,2)}s")
                
                print("\npress any key to go back to the main menu")
                word = input("> ").lower()
                if word.lower() == "q":
                    print("quit")
                    os.system("clear && printf '\\e[3J'")
                    reset_game_state()
                    break
            
                elif word.lower() == "hs":
                    os.system("clear && printf '\\e[3J'")
                    loadleaderboard(theme.strip(), theme)
                    input("\npress any key to quit")
                    reset_game_state()
                    break

                else:
                    os.system("clear && printf '\\e[3J'")
                    reset_game_state()
                    break
    
        
        
        elif word in hintwords and word not in found_words and lives > 0:
            
            os.system("clear && printf '\\e[3J'")            
            hints +=1
            found_words.add(word)
            foundhintwords.append(word)

            setupboard(letters, lives)
            print(f"\tHint word found! {word}")
            if hints == 3:
                hintmessage = "\tHINT AVAILABLE [Type 'hint' and press enter]"
                print(hintmessage)
            else:
                print(f"\tAccess a hint ({hints}/3)")
            print(f"Theme words found: ({themewordsfound}/6): {' '.join(themes)}")
            print(f"Hint words found: {' '.join(foundhintwords)}")
                
 
        elif word.lower() == "hint" and hints >= 3 and lives > 0:

            os.system("clear && printf '\\e[3J'")
            # hintmessage = "HINT AVAILABLE [Type 'hint' and press enter]"

            hintsused += 1
            hints = 0
            remaining_values = [value for key, value in themewords.items() if key not in found_words]
    
            if remaining_values:  # Ensure there are still unfound words left
                random_value = random.choice(remaining_values)
                highlighthint(random_value)  # Highlight the chosen word as a hint
            
            setupboard(letters, lives)
            # print(hintmessage)
            print(f"\tAccess a hint ({hints}/3)")
            print(f"Theme words found ({themewordsfound}/6): {' '.join(themes)}")
            print(f"Hint words found: {' '.join(foundhintwords)}")
        

        elif word in found_words:
            os.system("clear && printf '\\e[3J'")
            setupboard(letters, lives)
            
            print("WORD ALREADY FOUND")
            print(f"\tAccess a hint ({hints}/3)")
            print(f"Theme words found ({themewordsfound}/6): {' '.join(themes)}")
            print(f"Hint words found: {' '.join(foundhintwords)}")
        
        elif lives == 1:
            os.system("clear && printf '\\e[3J'")
            gameover = """\033[1;33m
\t ██████╗  █████╗ ███╗   ███╗███████╗     ██████╗ ██╗   ██╗███████╗██████╗ ██╗
\t██╔════╝ ██╔══██╗████╗ ████║██╔════╝    ██╔═══██╗██║   ██║██╔════╝██╔══██╗██║
\t██║  ███╗███████║██╔████╔██║█████╗      ██║   ██║██║   ██║█████╗  ██████╔╝██║
\t██║   ██║██╔══██║██║╚██╔╝██║██╔══╝      ██║   ██║╚██╗ ██╔╝██╔══╝  ██╔══██╗╚═╝
\t╚██████╔╝██║  ██║██║ ╚═╝ ██║███████╗    ╚██████╔╝ ╚████╔╝ ███████╗██║  ██║██╗
\t ╚═════╝ ╚═╝  ╚═╝╚═╝     ╚═╝╚══════╝     ╚═════╝   ╚═══╝  ╚══════╝╚═╝  ╚═╝╚═╝                                                                             
\033[1;37m"""         
            typewritereffect(gameover, delay=0.002)

            print("Access answers [Type 'view' to show answers]")
            print("To go back to main menu [Type 'quit']")
            
            viewall = input("> ").lower()
            if viewall == "view":
                reset_highlighting() #when the user already answered some theme words, reset the highlighted words so that the brackets will not double
                for i in range(0,6): #0-6 because the key-value pair in dictionary is 0-5
                    
                    highlight(i) #SHOW ALL THE ANSWERS
                setupboard(letters, lives=0)
                for key in themewords.keys():
                    print(key, end=", ")
            else:
                reset_game_state()
                break
            input("\npress any key to go back to main menu\n")
            reset_game_state()
            break

        
        elif word == "QUIT":
            reset_game_state()
            break
        

        else:
            os.system("clear && printf '\\e[3J'")
            lives -= 1
            setupboard(letters, lives)
            
            print(f"{word} not a recognized word")
            
            print(f"\tAccess a hint ({hints}/3)")
            print(f"Theme words found ({themewordsfound}/6): {' '.join(themes)}")
            print(f"Hint words found: {' '.join(foundhintwords)}")



def loadleaderboard(file, theme):
    
    with open(file, 'r') as f:
         lines = f.readlines()
    leaderboard = []
    for line in lines:
        name, hints_used, time = line.strip().split(',')
        leaderboard.append({"name": name, "hints": int(hints_used), "time": float(time)})

    #sort leaderboard by hints used (ascending) and time (ascending)
    leaderboard.sort(key=lambda x: (x["hints"], x["time"]))

    #display the leaderboard in a formatted table
    print(f"\033[1;32m   HIGH SCORES: {theme}\033[1;37m\n")
    print(f"{'NAME':<10} | {'HINTS USED':<10} | {'TIME (s)':<10}")
    print("-" * 33)
    for entry in leaderboard:
        print(f"{entry['name']:<10} | {entry['hints']:<10} | {entry['time']:<10.2f}")


