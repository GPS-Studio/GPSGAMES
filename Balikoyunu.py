import random, time, os, json
from datetime import date
from colorama import Fore, Style, init
import pyfiglet

init(autoreset=True)

DATA_FILE = "fishing_game_data.json"

rods = {
    "Normal Rod": {"can_catch": ["Rare", "Super Rare"], "durability": 10, "price": 50},
    "Pro Rod": {"can_catch": ["Rare", "Super Rare", "Epic", "Mysterious"], "durability": 20, "price": 200},
    "Professional Rod": {"can_catch": ["Rare", "Super Rare", "Epic", "Mysterious", "Legendary"], "durability": 30, "price": 500},
}

swords = {
    "Wooden Sword": {"damage": 10, "price": 100},
    "Iron Sword": {"damage": 25, "price": 250},
    "Dragon Sword": {"damage": 50, "price": 500},
}

baits = {
    "Low Quality Bait": {"duration": 15, "price": 10},
    "Quality Bait": {"duration": 10, "price": 25},
    "Super Bait": {"duration": 5, "price": 35},
    "Legendary Bait": {"duration": 2, "price": 70},
}

fishes = [
    {"name": "Anchovy", "rarity": "Rare", "price": 10},
    {"name": "Anchovy", "rarity": "Super Rare", "price": 20},
    {"name": "Anchovy", "rarity": "Epic", "price": 30},
    {"name": "Bass", "rarity": "Rare", "price": 15},
    {"name": "Bass", "rarity": "Super Rare", "price": 30},
    {"name": "Bonito", "rarity": "Epic", "price": 40},
    {"name": "Salmon", "rarity": "Mysterious", "price": 50},
    {"name": "Pufferfish", "rarity": "Legendary", "price": 100},
    {"name": "Dragonfish", "rarity": "Legendary", "price": 200},
]

maps = {
    "Starting Island": {"price": 0, "fish_bonus": 0},
    "Deep Sea Island": {"price": 200, "fish_bonus": 0.3},
    "Legendary Cove": {"price": 500, "fish_bonus": 0.6},
}

tasks_list = [
    {"description": "Catch 5 fish", "type": "catch_fish", "target": 5, "reward": 100},
    {"description": "Buy 1 Pro Rod", "type": "buy_rod", "target": "Pro Rod", "reward": 150},
    {"description": "Buy 3 Super Baits", "type": "buy_bait", "target": {"bait": "Super Bait", "amount": 3}, "reward": 120},
]

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def intro():
    clear()
    print(Fore.GREEN + pyfiglet.figlet_format("GPS STUDIO"))
    time.sleep(1)
    clear()

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
            if "baits" not in data:
                data["baits"] = {bait: 0 for bait in baits}
            if "boss_health" not in data:
                data["boss_health"] = 0
            if "boss_number" not in data:
                data["boss_number"] = 0
            if "boss_guess_chances" not in data:
                data["boss_guess_chances"] = 3
            if "current_sword" not in data:
                data["current_sword"] = None
            if "tasks" not in data:
                data["tasks"] = []
            if "current_island" not in data:
                data["current_island"] = "Starting Island"
            return data
    else:
        return {
            "money": 100,
            "inventory": {},
            "current_rod": "Normal Rod",
            "rod_durability": rods["Normal Rod"]["durability"],
            "current_sword": None,
            "baits": {bait: 0 for bait in baits},
            "login_date": str(date.today()),
            "boss_health": 0,
            "boss_number": 0,
            "boss_guess_chances": 3,
            "tasks": [],
            "current_island": "Starting Island",
        }

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

def choose_bait(data):
    print("\nYour Baits:")
    for bait, amount in data["baits"].items():
        print(f"- {bait}: {amount} pcs")
    choice = input("Which bait will you use? (Press ENTER to cancel): ").strip()
    if choice == "":
        print("You can't fish without bait! Opening market...")
        time.sleep(1)
        market(data)
        return None
    if choice in baits and data["baits"][choice] > 0:
        data["baits"][choice] -= 1
        return baits[choice]["duration"]
    else:
        print("No bait available or invalid choice!")
        return None

def fish(data):
    clear()
    print("-- FISHING --")
    if data["rod_durability"] <= 0:
        print(Fore.RED + "Your rod broke! Buy a new rod from the market!")
        input("Press ENTER to continue...")
        return
    duration = choose_bait(data)
    if duration is None:
        return
    print(f"Fishing with bait, wait {duration} seconds...")
    time.sleep(duration)
    rod = data["current_rod"]
    rod_allowed = rods[rod]["can_catch"]
    island_bonus = maps[data["current_island"]]["fish_bonus"]
    possible_fishes = [f for f in fishes if f["rarity"] in rod_allowed]
    if not possible_fishes or random.random() < (0.2 - island_bonus):
        print("No fish caught.")
    else:
        fish_caught = random.choice(possible_fishes)
        name = f"{fish_caught['rarity']} {fish_caught['name']}"
        data["inventory"][name] = data["inventory"].get(name, 0) + 1
        print(Fore.CYAN + f"🎣 You caught a {name}! Value: {fish_caught['price']} money")
    data["rod_durability"] -= 1
    save_data(data)
    input("Press ENTER to continue...")

def show_inventory(data):
    clear()
    print("-- Inventory --")
    if not data["inventory"]:
        print("Inventory is empty.")
    else:
        for item, amount in data["inventory"].items():
            print(f"{item}: {amount} pcs")
    input("Press ENTER to continue...")

def market(data):
    while True:
        clear()
        print("-- MARKET --")
        print(f"Money: {data['money']}")
        print("1. Buy Rod")
        print("2. Buy Bait")
        print("3. Buy Sword")
        print("4. Change Island")
        print("5. Exit")
        choice = input(">> ").strip()
        if choice == "1":
            print("\n-- Rods --")
            for name, info in rods.items():
                print(f"{name}: {info['price']} money")
            buy = input("Rod to buy: ").strip()
            if buy in rods:
                if data["money"] >= rods[buy]["price"]:
                    data["current_rod"] = buy
                    data["rod_durability"] = rods[buy]["durability"]
                    data["money"] -= rods[buy]["price"]
                    print(Fore.GREEN + f"{buy} purchased!")
                else:
                    print(Fore.RED + "Not enough money.")
            else:
                print(Fore.RED + "Invalid rod.")
            input("Press ENTER to continue...")
        elif choice == "2":
            print("\n-- Baits --")
            for name, info in baits.items():
                print(f"{name}: {info['price']} money - Stock: {data['baits'].get(name,0)}")
            buy = input("Bait to buy: ").strip()
            if buy in baits:
                if data["money"] >= baits[buy]["price"]:
                    data["baits"][buy] = data["baits"].get(buy,0) + 1
                    data["money"] -= baits[buy]["price"]
                    print(Fore.GREEN + f"{buy} purchased!")
                else:
                    print(Fore.RED + "Not enough money.")
            else:
                print(Fore.RED + "Invalid bait.")
            input("Press ENTER to continue...")
        elif choice == "3":
            print("\n-- Swords --")
            for name, info in swords.items():
                print(f"{name}: {info['price']} money")
            buy = input("Sword to buy: ").strip()
            if buy in swords:
                if data["money"] >= swords[buy]["price"]:
                    data["current_sword"] = buy
                    data["money"] -= swords[buy]["price"]
                    print(Fore.GREEN + f"{buy} purchased!")
                else:
                    print(Fore.RED + "Not enough money.")
            else:
                print(Fore.RED + "Invalid sword.")
            input("Press ENTER to continue...")
        elif choice == "4":
            print("\n-- Map (Islands) --")
            for island, info in maps.items():
                price = info["price"]
                print(f"{island} - {price} money")
            chosen_island = input("Island to travel to: ").strip()
            if chosen_island in maps:
                if chosen_island == data["current_island"]:
                    print("You are already here.")
                elif data["money"] >= maps[chosen_island]["price"]:
                    data["money"] -= maps[chosen_island]["price"]
                    data["current_island"] = chosen_island
                    print(Fore.GREEN + f"You traveled to {chosen_island}!")
                else:
                    print(Fore.RED + "Not enough money.")
            else:
                print(Fore.RED + "Invalid island.")
            input("Press ENTER to continue...")
        elif choice == "5":
            break
        else:
            print(Fore.RED + "Invalid choice.")
            input("Press ENTER to continue...")
        save_data(data)

def sell_fishes(data):
    clear()
    total = 0
    if not data["inventory"]:
        print("You have no fish to sell.")
    else:
        for name, amount in data["inventory"].items():
            for f in fishes:
                if f"{f['rarity']} {f['name']}" == name:
                    total += f["price"] * amount
        print(Fore.GREEN + f"You earned {total} money!")
        data["money"] += total
        data["inventory"] = {}
        save_data(data)
    input("Press ENTER to continue...")

def daily_reward(data):
    today = str(date.today())
    if data.get("login_date") != today:
        print(Fore.YELLOW + "🎁 Daily reward: 100 money")
        data["money"] += 100
        data["login_date"] = today
        save_data(data)
        input("Press ENTER to continue...")

def show_tasks(data):
    clear()
    if not data["tasks"]:
        print("No tasks for today.")
        input("Press ENTER to continue...")
        return
    print("-- Your Tasks --")
    for i, task in enumerate(data["tasks"], 1):
        status = "Completed" if task.get("completed", False) else "Pending"
        print(f"{i}. {task['description']} - {status}")
    input("Press ENTER to continue...")

def update_tasks(data):
    if not data["tasks"]:
        data["tasks"] = random.sample(tasks_list, 3)
        for task in data["tasks"]:
            task["completed"] = False
    for task in data["tasks"]:
        if task["completed"]:
            continue
        if task["type"] == "catch_fish":
            total_caught = sum(data["inventory"].values())
            if total_caught >= task["target"]:
                print(Fore.GREEN + f"Task completed: {task['description']}! Reward: {task['reward']} money")
                data["money"] += task["reward"]
                task["completed"] = True
        elif task["type"] == "buy_rod":
            if data["current_rod"] == task["target"]:
                print(Fore.GREEN + f"Task completed: {task['description']}! Reward: {task['reward']} money")
                data["money"] += task["reward"]
                task["completed"] = True
        elif task["type"] == "buy_bait":
            bait = task["target"]["bait"]
            amount = task["target"]["amount"]
            if data["baits"].get(bait, 0) >= amount:
                print(Fore.GREEN + f"Task completed: {task['description']}! Reward: {task['reward']} money")
                data["money"] += task["reward"]
                task["completed"] = True
    save_data(data)
    input("Press ENTER to continue...")

def boss_fight(data):
    clear()
    if data["current_sword"] is None:
        print(Fore.RED + "You must buy a sword from the market first!")
        input("Press ENTER to continue...")
        return

    if data["boss_health"] <= 0:
        data["boss_health"] = 50
        data["boss_number"] = random.randint(1, 5)
        data["boss_guess_chances"] = 3
        print(Fore.MAGENTA + "A new boss appeared! A hidden number between 1-5, guess and strike!")
        input("Press ENTER to continue...")

    while data["boss_health"] > 0 and data["boss_guess_chances"] > 0:
        guess = input("Your guess (1-5): ").strip()
        if not guess.isdigit() or not (1 <= int(guess) <= 5):
            print(Fore.RED + "Please enter a number between 1 and 5.")
            continue
        guess = int(guess)

        if guess == data["boss_number"]:
            damage = swords[data["current_sword"]]["damage"]
            data["boss_health"] -= damage
            print(Fore.GREEN + f"Congrats! You dealt {damage} damage to the boss. Remaining health: {data['boss_health']}")
            if data["boss_health"] <= 0:
                print(Fore.YELLOW + "Boss defeated! You earned a big reward of 500 money!")
                data["money"] += 500
                data["boss_health"] = 0
                data["boss_number"] = 0
                data["boss_guess_chances"] = 3
                save_data(data)
                input("Press ENTER to continue...")
                return
            else:
                save_data(data)
        else:
            data["boss_guess_chances"] -= 1
            print(Fore.RED + f"Wrong guess! Remaining guesses: {data['boss_guess_chances']}")
            if data["boss_guess_chances"] == 0:
                print(Fore.RED + "Your sword broke! You failed to guess the boss number.")
                data["current_sword"] = None
                data["boss_health"] = 0
                data["boss_number"] = 0
                data["boss_guess_chances"] = 3
                save_data(data)
                input("Press ENTER to continue...")
                return

def show_money(data):
    clear()
    print(f"💰 Your money: {data['money']}")
    input("Press ENTER to continue...")

def menu():
    intro()
    data = load_data()
    daily_reward(data)
    update_tasks(data)
    while True:
        clear()
        print(Fore.CYAN + f"Money: {data['money']} | Rod: {data['current_rod']} ({data['rod_durability']} durability) | Sword: {data['current_sword'] if data['current_sword'] else 'None'} | Island: {data['current_island']}")
        print("\n-- Main Menu --")
        print("1. Fish")
        print("2. Inventory")
        print("3. Market")
        print("4. Sell Fishes")
        print("5. Boss Fight")
        print("6. Map (Change Island)")
        print("7. Daily Tasks")
        print("8. Money Status")
        print("9. Exit")
        choice = input("Your choice: ").strip()

        if choice == "1":
            fish(data)
        elif choice == "2":
            show_inventory(data)
        elif choice == "3":
            market(data)
        elif choice == "4":
            sell_fishes(data)
        elif choice == "5":
            boss_fight(data)
        elif choice == "6":
            market(data)  # Island change is in market
        elif choice == "7":
            show_tasks(data)
        elif choice == "8":
            show_money(data)
        elif choice == "9":
            clear()
            print("Exiting the game, see you!")
            break
        else:
            print(Fore.RED + "Invalid choice!")
            input("Press ENTER to continue...")

if __name__ == "__main__":
    menu()