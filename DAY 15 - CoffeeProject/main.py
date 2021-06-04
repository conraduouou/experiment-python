# import modules
from resources import resources, MENU
from os import system


# to record user choice function
def command():
    """A function that records user choice"""
    to_print = """
    What would you like?
    COMMANDS:
        espresso/latte/cappuccino - flavors
        exit                      - to exit
        report                    - to check coffee resources
    
    Choice: """

    choice = input(to_print)

    # to ensure errors are catched
    while choice not in MENU and choice != "report" and choice != "exit":
        choice = input("Invalid input: ")

    return choice


def report(resources):
    """A function that prints out coffee machine resources"""
    print(f"Water: {resources['water']}ml")
    print(f"Milk: {resources['milk']}ml")
    print(f"Coffee: {resources['coffee']}g")
    print(f"Money: ${resources['money']}")


def calculate(resources, user_choice, coffee_menu):
    """A function that calculates user's coins and records money in resources"""

    print("Please insert coins:")
    quarters = float(input("How many quarters? "))
    dimes = float(input("How many dimes? "))
    nickels = float(input("How many nickels? "))
    pennies = float(input("How many pennies? "))

    total = (quarters * 0.25) + (dimes * 0.10) + (nickels * 0.05) + (pennies * 0.01)
    
    if total > coffee_menu[user_choice]["cost"]:
        change = total - coffee_menu[user_choice]["cost"]
        print(f"Here is ${change} in change.")
    elif total < coffee_menu[user_choice]["cost"]:
        print("Sorry that's not enough money. Money returned.")
        return
    
    total -= change
    resources["money"] += total
    print(f"Here is your {choice} ☕ Enjoy!")


system("cls")

# finished variable to indicate program finish
finished = False

while not finished:
    # user input to record coffee choice
    choice = command()

    # exit program
    if choice == "exit":
        finished = True
    elif choice == "report":
        report(resources)
    else:
        for item in MENU[choice]["ingredients"]:
            if resources[item] - MENU[choice]["ingredients"][item] < 0:
                print(f"Sorry, there is not enough {item}.")
                exit()
            else:
                resources[item] -= MENU[choice]["ingredients"][item]

        calculate(resources, choice, MENU)