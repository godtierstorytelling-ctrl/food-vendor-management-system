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
    "Test",
    "Member",
    "testmember@email.com",
    "1234567890",
    "password",
    "1111222233334444",
    "1028",
    "123 Test Street",
    30,
    0
)

# Put test member into the database
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


# ACT
vendor.order_food(customer)


# CHECK OBJECT
print()
print("MEMBER RESULT:")
print("Points:", customer.points)
print("History:", customer.history)


# CHECK DATABASE
db_customer = database.get_customer(customer.user_name)

print()
print("DATABASE RESULT:")
print("Points:", db_customer.points)
print("History:", db_customer.history)

database.disconnect()