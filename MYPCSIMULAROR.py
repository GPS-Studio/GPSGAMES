from colorama import*
import os
import time
import pyfiglet
import random

print(Fore.GREEN+pyfiglet.figlet_format("GPS SUTIDIO"))
time.sleep(0.5)
os.system('clear')
print(pyfiglet.figlet_format("WELCOME"))
time.sleep(0.5)
os.system('clear')
print(pyfiglet.figlet_format("THE"))
time.sleep(0.5)
os.system('clear')
print(pyfiglet.figlet_format("MY"))
time.sleep(0.5)
print(pyfiglet.figlet_format("PC"))
time.sleep(0.5)
print(pyfiglet.figlet_format("SIMULATOR"))
time.sleep(0.5)
os.system('clear')

print("'>Type 'help' to see all commands'")

while True:
    Mypc = input("mypc㉿localhost~$ ")

    if Mypc == "help":
        print("games   = open the games")
        print("papers  = open the papers")
        print("hack    = open the 'fake' hacks")
        print("exit    = exit program")
    elif Mypc == "exit":
        print("Exiting program. Bye!")
        break

    elif Mypc == "papers":
        print("Type 'exit' to return to main menu.")
        while True:
            papers = input("mypc㉿papers~$ ")
            if papers == "exit":
                os.system("clear")
                break
            else:
                print(f"Unknown papers command: {papers}")

    elif Mypc == "hack":
        print("Available hack commands: crack-password, inject-virus, trace-ip, help, exit")
        while True:
            Myhackp = input("mypc㉿hack~$  ")
            if Myhackp == "exit":
                os.system('clear')
                break
            elif Myhackp == "help":
                print(
                    "crack-password  → Tries to crack a password (fake)\n"
                    "inject-virus    → Injects a fake virus\n"
                    "trace-ip        → Pretends to trace an IP\n"
                    "help            → Show this help message\n"
                    "exit            → Return to main menu"
                )
            elif Myhackp == "crack-password":
                print("Cracking password...")
                time.sleep(2)
                print(random.randint(1,100))
                time.sleep(2)
                print(random.randint(1,100))
                time.sleep(2)
                print(random.randint(1,100))
            elif Myhackp == "inject-virus":
                print("Injecting virus...")
                time.sleep(2)
                print("💀 SYSTEM CORRUPTED 💀 (just kidding)")
            elif Myhackp == "trace-ip":
                print("Tracing IP...")
                time.sleep(2)
                print("Target located: 192.168.1.7")
            else:
                print("Unknown hack command. Type 'help' for list of commands.")

    elif Mypc == "games":
        print("Available games: guess-number, rock-paper-scissors, password-breaker, help, exit")
        while True:
            game = input("mypc㉿games~$  ")

            if game == "exit":
                os.system('clear')
                break

            elif game == "help":
                print(
                    "guess-number         → Guess a number between 1-10\n"
                    "rock-paper-scissors  → Play rock-paper-scissors\n"
                    "password-breaker     → Try to guess a 3-digit code\n"
                    "exit                 → Return to main menu"
                )

            elif game == "guess-number":
                number = random.randint(1, 10)
                print("🎯 Guess a number between 1 and 10")
                while True:
                    guess = input("Your guess: ")
                    if not guess.isdigit():
                        print("Please enter a number.")
                        continue
                    guess = int(guess)
                    if guess == number:
                        print("🎉 Correct! You win!")
                        break
                    else:
                        print("❌ Wrong! Try again.")

            elif game == "rock-paper-scissors":
                choices = ["rock", "paper", "scissors"]
                while True:
                    user = input("Choose rock, paper, or scissors (or type 'exit'): ").lower()
                    if user == "exit":
                        break
                    if user not in choices:
                        print("Invalid choice.")
                        continue
                    cpu = random.choice(choices)
                    print(f"🖥️ CPU chose: {cpu}")
                    if user == cpu:
                        print("🤝 It's a draw!")
                    elif (user == "rock" and cpu == "scissors") or (user == "scissors" and cpu == "paper") or (user == "paper" and cpu == "rock"):
                        print("🏆 You win!")
                    else:
                        print("💀 You lose!")

            elif game == "password-breaker":
                code = str(random.randint(100, 999))
                print("🔐 Try to break the 3-digit password!")
                attempts = 0
                while True:
                    guess = input("Enter code (or 'exit'): ")
                    if guess == "exit":
                        break
                    if len(guess) != 3 or not guess.isdigit():
                        print("❗ Must be a 3-digit number.")
                        continue
                    attempts += 1
                    if guess == code:
                        print(f"✅ Code cracked in {attempts} tries!")
                        break
                    else:
                        hints = []
                        for i in range(3):
                            if guess[i] == code[i]:
                                hints.append("✔")
                            elif guess[i] in code:
                                hints.append("?")
                            else:
                                hints.append("✖")
                        print("Hint:", " ".join(hints))
            else:
                print("Unknown game command. Type 'help' to see available games.")

    else:
        print(f"Unknown command: {Mypc}. Type 'help' to see all commands.")