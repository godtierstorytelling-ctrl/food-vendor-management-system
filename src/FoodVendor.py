from datetime import datetime

class FoodVendor:

    def __init__(self):
        self.db = None
        self.receipt_number = 1000

    def initialize(self, database):
        self.db = database
        self.db.connect()
        self.db.create_menu_table("menu.tsv")
        self.db.create_user_table("user.tsv")

    def admin_login(self, database=None):
        active_db = database if database is not None else self.db
        attempts = 0
        while attempts < 3:
            user_name = input("Please enter your user_name: ")
            password = input("Please enter your password: ")

            user = active_db.get_admin(user_name)

            # Safe check added here too
            if user is not None and user.user_name == user_name and user.password == password:
                return user

            attempts += 1
            if attempts == 3:
                print(
                    "You have reached the maximum number of "
                    "login attempts. Goodbye!"
                )
                return None

            print(
                "Admin account not found or password mismatch! "
                "Please check your user_name and password."
            )

    def customer_login(self, database):
        active_db = database if database is not None else self.db

        attempts = 0

        while attempts < 3:
            user_name = input("Please enter your user_name: ")
            password = input("Please enter your password: ")

            user = active_db.get_customer(user_name)

            if user is not None and user.user_name == user_name and user.password == password:
                return user

            attempts += 1

            if attempts == 3:
                print(
                    "You have reached the maximum number of "
                    "login attempts. Goodbye!"
                )
                return None

            print(
                "Customer account not found or password mismatch! "
                "Please check your user_name and password."
            )

    def create_receipt(self, items, user, reward):
        self.receipt_number += 1

        file_name = f"FoodVendorReceipt{self.receipt_number}.txt"

        subtotal = 0
        wait_time = 0

        for item in items:
            subtotal += self.db.get_food_price(item)
            wait_time += self.db.get_food_time(item)

        reward_value = reward * 0.10
        total = subtotal - reward_value

        with open(file_name, "w") as receipt:
            receipt.write(f"{'FOOD VENDOR':^21}\n\n\n")

            receipt.write(f"{user}\n")
            receipt.write(f"Receipt #: {self.receipt_number}\n")

            current_time = datetime.now()

            receipt.write(
                current_time.strftime("%a, %m/%d/%y, %I:%M:%S %p")
                + "\n\n"
            )

            receipt.write(f"{'Items':<25}Price\n")
            receipt.write("--------------------------------\n")

            for item in items:
                price = self.db.get_food_price(item)
                receipt.write(
                    f"{item:<25}${price:5.2f}\n"
                )

            receipt.write("--------------------------------\n")

            if user.user_name == "Guest":
                receipt.write(
                    f"{'Total:':>25}  ${total:5.2f}\n"
                )

            else:
                receipt.write(
                    f"{'Subtotal:':>24}  ${subtotal:5.2f}\n"
                )
                receipt.write(
                    f"{'Rewards:':>24} -${reward_value:5.2f}\n"
                )
                receipt.write("--------------------------------\n")
                receipt.write(
                    f"{'Total:':>24}  ${total:5.2f}\n"
                )

            receipt.write("\n")

            last_four = user.card_num[-4:]

            receipt.write(
                f"Credit card: xxxx xxxx xxxx {last_four}\n\n"
            )

            if user.user_name != "Guest":
                points_earned = int(total * 0.05)

                receipt.write(
                    f"You've earned {points_earned} points "
                    "from this order!\n\n"
                )

                user.points = user.points - reward + points_earned
                user.history = self.receipt_number

                self.db.update_customer_rewards(
                    user.user_name,
                    user.points
                )

                self.db.update_customer_history(
                    user.user_name,
                    user.history
                )

            receipt.write(
                f"Your order will be ready in: {wait_time} mins.\n"
            )

            receipt.write("Thank you for your order!\n")

    def print_order_history(self,user):
        customer = self.db.get_customer(user.user_name)

        receipt_number = customer.history

        file_name = f"FoodVendorReceipt{receipt_number}.txt"

        with open(file_name, "r") as receipt:
            print(receipt.read())

    def order_food(self, user):
        order = []

        categories = {
            "1": "Sandwiches",
            "2": "Salads",
            "3": "Vegetarian",
            "4": "Mexican food",
            "5": "Drinks"
        }

        option_categories = {
            "Sandwiches": "Sandwiches_option",
            "Salads": "Salads_option",
            "Vegetarian": "Vegetarian_option",
            "Mexican food": "Mexican_option"
        }

        choice = ""

        while choice != "6":
            print()
            print("Daily Menu")
            print()
            print("Choose a category:")
            print("     Sandwiches - Enter 1")
            print("     Salads - Enter 2")
            print("     Vegetarian - Enter 3")
            print("     Mexican food - Enter 4")
            print("     Drink - Enter 5")
            print("     Check-out or exit - Enter 6")

            choice = input()

            while choice not in ("1", "2", "3", "4", "5", "6"):
                choice = input()

            if choice == "6":
                break

            category = categories[choice]

            self.db.display_daily_menu(category)

            item_name = input(
                'Enter the name of item you\'d like to order, '
                'or "None" to return to the previous menu. '
            )

            if item_name == "None":
                continue

            if (
                self.db.is_food_exist(item_name)
                and self.db.is_food_available(item_name)
            ):
                order.append(item_name)
                print(f"{item_name} added to order.")

                if category != "Drinks":
                    option_category = option_categories[category]

                    print()
                    print(
                        "Would you like to add any of these "
                        "options to your order?"
                    )

                    self.db.display_daily_menu(option_category)

                    option_name = input(
                        "Enter the name of option item you'd like "
                        'to order, or "None" to return to the '
                        "previous menu. "
                    )

                    if option_name != "None":
                        if (
                            self.db.is_food_exist(option_name)
                            and self.db.is_food_available(option_name)
                        ):
                            order.append(option_name)
                            print(f"{option_name} added to order.")
        if len(order) == 0:
            return

        reward = 0

        if user.user_name == "Guest":
            user.card_num = input(
                "Please enter a credit card number "
                "(no spaces or dashes): "
            )
            user.card_date = input(
                "Please enter an expiration date (MMYY): "
            )
            user.address = input(
                "Please enter a billing address: "
            )
            user.phone_num = input(
                "Please enter a phone number "
                "(no spaces or dashes): "
            )
            user.email = input(
                "Please enter an email address: "
            )

        else:
            print(
                f"You currently have {user.points} Reward Points. "
                "Please enter the number of Reward Points "
                "you want to redeem.",
                end=" "
            )

            reward_input = input()

            while(
                not reward_input.isdigit()
                or int(reward_input) > user.points
            ):
                reward_input = input(
                    "Please enter a valid number of Reward Points: "
                )

            reward = int(reward_input)

        self.create_receipt(order, user, reward)

        print(
            "Your order has been placed. "
            "Please take your receipt."
        )

    def main_menu(self):
        print("Welcome to the Food Vendor!")
        print("Choose an option to begin.")
        print("     Customer login - Enter 1")
        print("     Place an order as a guest - Enter 2")
        print("     Manage system (admin sign-in required) - Enter 3")
        print("     Leave the Food Vendor - Enter 4")

        choice = input()

        while choice not in ("1", "2", "3", "4"):
            choice = input()

        return int(choice)

    def member_menu(self, user):
        choice = ""

        while choice != "4":
            print(f"Welcome back, {user.first_name}!")
            print(
                f"You have {user.points} points in reward. "
                "Don't forget to use them!"
            )
            print("What would you like to do?")
            print("     Place an order - Enter 1")
            print("     View last order history - Enter 2")
            print("     Update profile - Enter 3")
            print("     Logout and return to main menu - Enter 4")

            choice = input()

            while choice not in ("1", "2", "3", "4"):
                print("Please enter a valid option (1 - 4):")
                print("     Place an order - Enter 1")
                print("     View last order history - Enter 2")
                print("     Update profile - Enter 3")
                print("     Logout and return to main menu - Enter 4")
                choice = input()

            if choice == "1":
                self.order_food(user)
                return

            elif choice == "2":
                self.print_order_history(user)

            elif choice == "3":
                user.update_customer_profile(user, self.db)

if __name__ == "__main__":
    from DbManager import DbManager
    from Users import Customer

    database = DbManager()

    vendor = FoodVendor()
    vendor.initialize(database)

    choice = 0

    while choice != 4:
        choice = vendor.main_menu()

        if choice == 1:
            user = vendor.customer_login(database)

            if user is None:
                break

            vendor.member_menu(user)

        elif choice == 2:
            guest = Customer()
            vendor.order_food(guest)

        elif choice == 3:
            user = vendor.admin_login(database)

            if user is None:
                break

            user.admin_menu(database)

        elif choice == 4:
            print("See you next time!")

    database.disconnect()
