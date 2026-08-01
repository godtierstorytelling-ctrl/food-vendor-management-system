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

customer = Customer(
    "testmember",
    "customer",
    "Gwion",
    "Tester",
    "gwion@email.com",
    "1234567890",
    "password",
    "1111222233334444",
    "1028",
    "123 Test Street",
    30,
    0
)

test_user = (
    customer.user_name,
    customer.account,
    customer.first_name,
    customer.last_name,
    customer.email,
    customer.phone_num,
    customer.password,
    "",
    customer.card_num,
    customer.card_date,
    customer.address,
    customer.points,
    customer.history
)

database.insert_user(test_user)


# CREATE AN ORDER HISTORY RECEIPT
items = [
    "Cheeseburger",
    "Double meat"
]

vendor.create_receipt(
    items,
    customer,
    10
)


# ACT
vendor.member_menu(customer)


database.disconnect()