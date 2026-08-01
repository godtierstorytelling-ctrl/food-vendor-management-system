from unittest.mock import patch

from DbManager import DbManager
from FoodVendor import FoodVendor
from Users import Admin


database = DbManager()
food_vendor = FoodVendor()

try:
    food_vendor.initialize(database)

    username = "admin"
    password = "password"

    retrieved_admin = database.get_admin(username)

    print("DATABASE VALUES:")
    print("Username:", repr(retrieved_admin.user_name))
    print("Account:", repr(retrieved_admin.account))
    print("Password:", repr(retrieved_admin.password))

    print("\nCOMPARISONS:")
    print("Username found:", retrieved_admin.user_name != "")
    print("Account is admin:", retrieved_admin.account == "admin")
    print("Password matches:", retrieved_admin.password == password)

    with patch("builtins.input", side_effect=[username, password]):
        result = food_vendor.admin_login()

    print("\nLOGIN RESULT:")
    print(result)
    print("Is Admin:", isinstance(result, Admin))

finally:
    database.disconnect()