from DbManager import DbManager
from FoodVendor import FoodVendor
from Users import Customer


# ARRANGE
database = DbManager()
database.connect()
database.create_menu_table("menu.tsv")
database.create_user_table("user.tsv")

vendor = FoodVendor()
vendor.db = database

guest = Customer()


# ACT
vendor.order_food(guest)


# CHECK
print()
print("GUEST INFORMATION:")
print("Card:", guest.card_num)
print("Expiration:", guest.card_date)
print("Address:", guest.address)
print("Phone:", guest.phone_num)
print("Email:", guest.email)

database.disconnect()