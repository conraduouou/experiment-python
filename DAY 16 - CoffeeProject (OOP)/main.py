from menu import Menu, MenuItem
from coffee_maker import CoffeeMaker
from money_machine import MoneyMachine


# missing method in menu
def in_menu(menu, choice):
    for item in menu.menu:
        if item.name == choice:
            return True
    return False

# make respective objects
items = Menu()
cash_machine = MoneyMachine()
coffee_vendor = CoffeeMaker()

finished = False

while not finished:
    # ask for user choice
    choice = input(f"What would you like? ({items.get_items()}): ")

    # to ensure user always choose among the three options
    while not in_menu(items, choice) and choice != "report":
        choice = input("Invalid input. Follow the instructions above: ")

    if choice == "report":
        coffee_vendor.report()
        cash_machine.report()
    else:
        # Instantiate object
        coffee = items.find_drink(choice)

        if coffee_vendor.is_resource_sufficient(coffee):
            if cash_machine.make_payment(coffee.cost):
                coffee_vendor.make_coffee(coffee)