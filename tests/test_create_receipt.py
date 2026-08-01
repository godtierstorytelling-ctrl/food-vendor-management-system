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
    "testcustomer",
    "customer",
    "Test",
    "Customer",
    "test@email.com",
    "1234567890",
    "password",
    "1111222233334444",
    "1028",
    "123 Test Street",
    30,
    0
)

items = [
    "Cheeseburger",
    "Double meat"
]

# ACT
vendor.create_receipt(
    items,
    customer,
    10
)

# ASSERT / INSPECT
print("Receipt number:", vendor.receipt_number)
print("Customer points:", customer.points)
print("Customer history:", customer.history)

with open("FoodVendorReceipt1001.txt", "r") as file:
    print()
    print(file.read())

database.disconnect()