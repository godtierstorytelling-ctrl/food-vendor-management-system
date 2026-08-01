class User:
    def __init__(self, user_name, account, first_name, last_name, email, phone_num, password):
        self.user_name = user_name
        self.account = account
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone_num = phone_num
        self.password = password

class Admin(User):
    def __init__(self, user_name, account, first_name, last_name, email, phone_num, password, id):
            super().__init__(user_name, account, first_name, last_name, email, phone_num, password)
            self.employ_id = id
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}: {self.user_name}, Employee ID: {self.employ_id}"

    def update_admin_profile(self, database):
        print(f"Current user profile for {self.user_name}:")
        print()
        print(f" Phone number: {self.phone_num}")
        print(f" Email address: {self.email}")
        print()
        self.phone_num = input("Please enter a phone number (no spaces or dashes): ")
        self.email = input("Please enter an email address: ")
        database.update_admin(self)

    def create_account(self, database):
        user_name = input("Please enter the user_name of the new account: ")
        while database.is_user_exist(user_name):
            user_name = input(f"{user_name} is not available, please choose a different user_name: ")
            
        password = input("Please enter a new password: ")
        account_type = input("Is this a customer account (Y/N)? ")
        first_name = input("Please enter the first name: ")
        last_name = input("Please enter the last name: ")
        email = input("Please enter an email address: ")
        phone_num = input("Please enter a phone number: ")
        
        if account_type == "Y":
            card_num = input("Please enter a credit card number (no spaces or dashes): ")
            card_date = input("Please enter an expiration date (MMYY): ")
            address = input("Please enter a billing address: ")
            new_user = (user_name, "customer", first_name, last_name, email, phone_num, password, "", card_num, card_date, address, 0, 0)
        else:
            employee_id = input("Please enter employee ID: ")
            new_user = (user_name, "admin", first_name, last_name, email, phone_num, password, employee_id, "", "", "", 0, 0)
            
        database.insert_user(new_user)

    def delete_account(self, database):
        user_name = input(
            "Please enter the user_name of the account to be deleted: "
        )

        while (
            not database.is_user_exist(user_name)
            or user_name == self.user_name
        ):
            user_name = input(
                "Please enter the user_name of the account to be deleted: "
            )

        confirmation = input(
            f"Account of {user_name} will be removed. "
            "Are you sure (Y/N)? "
        )

        if confirmation == "Y":
            database.delete_user(user_name)
            print(f"Account of {user_name} removed.")
    
    def manage_accounts(self, database):
        choice = ""
        while choice != "5":
            print("Manage accounts - choose an option:")
            print(" Update your profile - Enter 1")
            print(" Update customer profile - Enter 2")
            print(" Create an account - Enter 3")
            print(" Delete an account - Enter 4")
            print(" Return to employee menu - Enter 5")
            choice = input()
            while choice not in ("1", "2", "3", "4", "5"):
                choice = input()
                
            if choice == "1":
                self.update_admin_profile(database)
            elif choice == "2":
                print("Manage Customer Profile")
                user_name = input("Please enter the user_name of customer: ")
                while not database.is_user_exist(user_name):
                    print("Customer not found.")
                    user_name = input("Please enter the user_name of customer: ")
                customer = database.get_customer(user_name)
                if customer is not None:
                    customer.update_customer_profile(database)
                else:
                    print("Customer not found.")
            elif choice == "3":
                self.create_account(database)
            elif choice == "4":
                self.delete_account(database)

    def insert_food_item(self, database):
        print("Please choose a food category:")
        print("     Sandwiches - Enter 1")
        print("     Salads - Enter 2")
        print("     Drinks - Enter 3")
        print("     Mexican food - Enter 4")
        print("     Vegetarian - Enter 5")
        print("     Return to previous menu - Enter 6")

        choice = input()

        while choice not in ("1", "2", "3", "4", "5", "6"):
            choice = input()

        if choice == "6":
            return

        categories = {
            "1": "Sandwiches",
            "2": "Salads",
            "3": "Drinks",
            "4": "Mexican food",
            "5": "Vegetarian"
        }

        category = categories[choice]

        if category != "Drinks":
            side_option = input("Is this a side option (Y/N)? ")

            if side_option == "Y":
                if category == "Mexican food":
                    category = "Mexican_option"
                else:
                    category = category + "_option"

        item_name = input("Please enter the name of the food item: ")
        description = input("Please enter the description of food item: ")
        price = float(input("Please enter the price of the food item: "))
        prep_time = int(
            input("Please enter the prep time of the food item (in minutes): ")
        )

        available_choice = input(
            "Do you want to make this item available in the daily menu (Y/N)? "
        )

        if available_choice == "Y":
            available = 1
        else:
            available = 0

        new_item = (
            category,
            item_name,
            description,
            price,
            prep_time,
            available
        )

        database.insert_menu(new_item)

    def manage_menu(self, database):
        choice = ""

        while choice != "5":
            print("Manage Food menu - choose an option:")
            print("     Insert new food item - Enter 1")
            print("     Update food price - Enter 2")
            print("     Update food description - Enter 3")
            print("     Update food availability for daily menu -  Enter 4")
            print("     Return to employee menu - Enter 5")

            choice = input()

            while choice not in ("1", "2", "3", "4", "5"):
                choice = input()

            if choice == "1":
                self.insert_food_item(database)

            elif choice == "2":
                item_name = input(
                    "Enter the name of the item for price change: "
                )

                while not database.is_food_exist(item_name):
                    item_name = input(
                        f"{item_name} is not on the menu, "
                        "please enter an item on the menu: "
                    )

                new_price = float(
                    input("Enter new price: ")
                )

                database.set_food_price(
                    item_name,
                    new_price
                )

            elif choice == "3":
                item_name = input(
                    "Enter the name of the item for description change: "
                )

                while not database.is_food_exist(item_name):
                    item_name = input(
                        f"{item_name} is not on the menu, "
                        "please enter an item on the menu: "
                    )

                new_description = input(
                    "Enter new description: "
                )

                database.set_food_description(
                    item_name,
                    new_description
                )

            elif choice == "4":
                item_name = input(
                    "Enter the name of the item for availability changes: "
                )

                while not database.is_food_exist(item_name):
                    item_name = input(
                        f"{item_name} is not on the menu, "
                        "please enter an item on the menu: "
                    )

                available_choice = input(
                    "Make this item available in the daily menu (Y/N)? "
                )

                if available_choice == "Y":
                    availability = 1
                else:
                    availability = 0

                database.set_food_availability(
                    item_name,
                    availability
                )
            pass

    def admin_menu(self, database):
        choice = ""

        while choice != "3":
            print(self)
            print()
            print("Admin menu - What would you like to do?")
            print("     Manage user accounts - Enter 1")
            print("     Manage food menu - Enter 2")
            print("     Logout and return to main menu - Enter 3")

            choice = input()

            while choice not in ("1", "2", "3"):
                choice = input()

            if choice == "1":
                self.manage_accounts(database)

            elif choice == "2":
                self.manage_menu(database)

class Customer(User):
    def __init__(self, user_name="Guest", account="", first_name="", last_name="", email="", phone_num="", password="", card_num="", card_date="", address="", points=0, history=0):
        super().__init__(user_name, account, first_name, last_name, email, phone_num, password)
        self.card_num = card_num
        self.card_date = card_date
        self.address = address
        self.points = points
        self.history = history

    def __str__(self):
        return f"{self.first_name} {self.last_name}: {self.user_name}, Rewards: {self.points}"

    def update_customer_profile(self, user, database=None):
        active_db = database
        target_user = self

        print(f"Current user profile for {self.user_name}:")
        print(f" Credit card number: {self.card_num}")
        print(f" Expiration date: {self.card_date}")
        print(f" Billing address: {self.address}")
        print(f" Phone number: {self.phone_num}")
        print(f" Email address: {self.email}")

        self.card_num = input("Please enter a credit card number (no spaces or dashes): ")
        self.card_date = input("Please enter an expiration date (MMYY): ")
        self.address = input("Please enter a billing address: ")
        self.phone_num = input("Please enter a phone number (no spaces or dashes): ")
        self.email = input("Please enter an email address: ")

        if active_db is not None:
            active_db.update_customer(self)
