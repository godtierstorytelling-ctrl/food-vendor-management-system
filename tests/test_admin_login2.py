# test_admin_login.py

from io import StringIO
from unittest.mock import patch

from DbManager import DbManager
from FoodVendor import FoodVendor


database = DbManager()
food_vendor = FoodVendor()

try:
    food_vendor.initialize(database)

    test_inputs = [
        "abcdefg",
        "1234567",
        "gwarner653",
        "zJk@rAvu4a",
        "rebradshaw835",
        "1234567"
    ]

    with patch("builtins.input", side_effect=test_inputs), \
         patch("sys.stdout", new_callable=StringIO) as output:

        result = food_vendor.admin_login()
        actual_output = output.getvalue()

    print("RETURN VALUE:")
    print(repr(result))

    print("\nCAPTURED OUTPUT:")
    print(repr(actual_output))

finally:
    database.disconnect()