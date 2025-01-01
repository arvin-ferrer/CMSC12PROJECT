from load import *

def menu():
    os.system("clear && printf '\\e[3J'")
    terminalsize = os.get_terminal_size().columns
    menumessage="""
\033[1;32m
\t\t                          WELCOME TO    
\t\t███████╗████████╗██████╗  █████╗ ███╗   ██╗██████╗ ███████╗
\t\t██╔════╝╚══██╔══╝██╔══██╗██╔══██╗████╗  ██║██╔══██╗██╔════╝
\t\t███████╗   ██║   ██████╔╝███████║██╔██╗ ██║██║  ██║███████╗
\t\t╚════██║   ██║   ██╔══██╗██╔══██║██║╚██╗██║██║  ██║╚════██║
\t\t███████║   ██║   ██║  ██║██║  ██║██║ ╚████║██████╔╝███████║
\t\t╚══════╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═════╝ ╚══════╝
\t\t"""

    typewritereffect(menumessage, delay=0.002)


def loading_animation():
    frames = [
        "\033[1;32m[     ]\033[0m Loading...",
        "\033[1;32m[=    ]\033[0m Loading...",
        "\033[1;32m[==   ]\033[0m Loading...",
        "\033[1;32m[===  ]\033[0m Loading...",
        "\033[1;32m[ ==== ]\033[0m Loading...",
        "\033[1;32m[  ====]\033[0m Loading...",
        "\033[1;32m[   ===]\033[0m Loading...",
        "\033[1;32m[    ==]\033[0m Loading...",
        "\033[1;32m[     =]\033[0m Loading...",
        "\033[1;32m[      ]\033[0m Loading..."
    ]

    for _ in range(3):  #repeat the animation 3 times
        for frame in frames:
            sys.stdout.write(f"\r{frame}")
            sys.stdout.flush()
            time.sleep(0.2)

    sys.stdout.write("\r" + " " * len(frames[0]) + "\r")
    



def help():
    
    print("\033[1;37m\n\n\t\tHere are some commands for you to try out:\n")
    print("\033[1;32m\t\t- Play -", end=" ")
    print("\033[1;37m \t\t\tto start playing")
    print("\033[1;32m\t\t- Mode -", end=" ")
    print("\033[1;37m \t\t\tto choose a theme (default theme is [1])")
    print("\033[1;32m\t\t- Score -", end=" ")
    print("\033[1;37m \t\t\tview leaderboard")
    print("\033[1;32m\t\t- Help -", end=" ")
    print("\033[1;37m \t\t\tview this message again")
    print("\033[1;32m\t\t- Quit -", end=" ")
    print("\033[1;37m \t\t\tto quit the game\n")

def choosemode():
    global mode
    os.system("clear && printf '\\e[3J'")
    print("\033[1;32mChoose a puzzle:\033[1;37m\n")
    print("[1] Let's experiment")
    print("[2] To your health")
    print("[3] Good on paper")
    print("\npress any key to choose the default option(1)\n")
    mode = input("> ")
    if mode == "1":
        print("Selected puzzle: Let's experiment")
        # time.sleep(1)
        mode = "letsexperiment.txt"
        
    elif mode == "2":

        print("Selected puzzle: To your health!")
        # time.sleep(1)
        mode = "toyourhealth.txt"
        
    elif mode == "3":
        print("Selected puzzle: Good on paper")
        # time.sleep(1.5)
        mode = "goodonpaper.txt"
        
    else:
        print("Selected puzzle: Let's experiment")
        # time.sleep(1)
        mode = "letsexperiment.txt"
    time.sleep(1.3) #adjust when the delay is too slow/fast


def main(theme):
    # userlogin()
    global mode
    
    menu()
    help()
    while True:
        
        choice = input(">> ").lower()
        if choice == "play":
            if mode == "": #when the user doesn't choose a puzzle choose the default theme
                print("PLEASE WAIT")
                loading_animation()
                # time.sleep(5)
                load("letsexperiment.txt")
            else:
                load(mode)
            setupboard(letters, lives)
            play(hints, themewordsfound, hintmessage, hintsused, lives)
            os.system("clear && printf '\\e[3J'")
            menu()
            help()
        elif choice == "mode":
            
            choosemode()
            os.system("clear && printf '\\e[3J'")
            menu()
            help()
        elif choice == "score":
            # load()
            os.system("clear && printf '\\e[3J'")
   
            print("""
Choose scoreboard to view:
[1] Let's experiment
[2] To your health
[3] Good on paper

press any key to choose the default option(1)                  
""")
            scoreboard = input("> ")
            os.system("clear && printf '\\e[3J'")
            if scoreboard == "1":
                theme = "Let's experiment"

                loadleaderboard("Let's experiment", theme)
            elif scoreboard == "2":
                theme = "To your health!"
      
                loadleaderboard("To your health!", theme)
            elif scoreboard == "3":
                theme = "Good on paper"

                loadleaderboard("Good on paper", theme)
            else:
                theme = "Let's experiment"
                
                loadleaderboard("Let's experiment", theme)
            input("\npress any key to quit\n")
            os.system("clear && printf '\\e[3J'")
            menu()
            help()
        
        elif choice == "help":

            os.system("clear && printf '\\e[3J'")
            menu()
            help()
        
        elif choice == "quit":
            print("\033[1;32mThanks for playing :)")
            break
        
        else:    
            print(f"{choice}: command not found...")
            

main(theme)
