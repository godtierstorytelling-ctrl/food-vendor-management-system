from contextlib import redirect_stdout
from io import StringIO
from unittest.mock import patch

from DbManager import DbManager
from FoodVendor import FoodVendor
from Users import Customer


def test_customer_login():
    database = DbManager()
    food_vendor = FoodVendor()

    try:
        food_vendor.initialize(database)

        cursor = database.conn.cursor()

        # Find one valid customer account.
        cursor.execute(
            """
            SELECT user_name, password
            FROM user
            WHERE account_type = 'customer'
            LIMIT 1
            """
        )

        customer_row = cursor.fetchone()

        assert customer_row is not None, (
            "No customer account was found in user.tsv."
        )

        customer_user_name = customer_row[0]
        customer_password = customer_row[1]

        # Find one administrator so we can verify that an admin
        # cannot authenticate through customer_login().
        cursor.execute(
            """
            SELECT user_name, password
            FROM user
            WHERE account_type = 'admin'
            LIMIT 1
            """
        )

        admin_row = cursor.fetchone()

        assert admin_row is not None, (
            "No administrator account was found in user.tsv."
        )

        admin_user_name = admin_row[0]
        admin_password = admin_row[1]

        # -----------------------------------------------------
        # TEST 1: VALID CUSTOMER LOGIN
        # -----------------------------------------------------

        with patch(
            "builtins.input",
            side_effect=[
                customer_user_name,
                customer_password
            ]
        ):
            result = food_vendor.customer_login()

        assert result is not None
        assert isinstance(result, Customer)
        assert result.user_name == customer_user_name
        assert result.account == "customer"
        assert result.password == customer_password
        assert result.db is database

        print("PASS: Valid credentials returned a Customer object.")

        # -----------------------------------------------------
        # TEST 2: FAILED ATTEMPT FOLLOWED BY SUCCESS
        # -----------------------------------------------------

        output = StringIO()

        with patch(
            "builtins.input",
            side_effect=[
                customer_user_name,
                "wrong_password",
                customer_user_name,
                customer_password
            ]
        ):
            with redirect_stdout(output):
                result = food_vendor.customer_login()

        displayed_output = output.getvalue()

        assert isinstance(result, Customer)
        assert result.user_name == customer_user_name

        assert (
            "Username or password does not match."
            in displayed_output
        )

        assert (
            "You have reached the maximum number of "
            "login attempts. Goodbye!"
            not in displayed_output
        )

        print("PASS: Failed attempt displayed the mismatch message.")
        print("PASS: A later valid attempt returned the Customer.")

        # -----------------------------------------------------
        # TEST 3: ADMIN CANNOT LOG IN AS CUSTOMER
        # -----------------------------------------------------

        output = StringIO()

        with patch(
            "builtins.input",
            side_effect=[
                admin_user_name,
                admin_password,
                customer_user_name,
                customer_password
            ]
        ):
            with redirect_stdout(output):
                result = food_vendor.customer_login()

        displayed_output = output.getvalue()

        assert isinstance(result, Customer)
        assert result.user_name == customer_user_name
        assert result.account == "customer"

        assert (
            "Username or password does not match."
            in displayed_output
        )

        print("PASS: Admin credentials were rejected.")
        print("PASS: Customer credentials worked on the next attempt.")

        # -----------------------------------------------------
        # TEST 4: MISSING USERNAME IS REJECTED
        # -----------------------------------------------------

        output = StringIO()

        with patch(
            "builtins.input",
            side_effect=[
                "not_a_real_customer",
                "not_a_real_password",
                customer_user_name,
                customer_password
            ]
        ):
            with redirect_stdout(output):
                result = food_vendor.customer_login()

        displayed_output = output.getvalue()

        assert isinstance(result, Customer)
        assert result.user_name == customer_user_name

        assert (
            "Username or password does not match."
            in displayed_output
        )

        print("PASS: Missing customer account was rejected.")
        print("PASS: Login continued after the missing username.")

        # -----------------------------------------------------
        # TEST 5: THREE FAILED ATTEMPTS
        # -----------------------------------------------------

        output = StringIO()

        with patch(
            "builtins.input",
            side_effect=[
                customer_user_name,
                "wrong_password_1",
                customer_user_name,
                "wrong_password_2",
                customer_user_name,
                "wrong_password_3"
            ]
        ):
            with redirect_stdout(output):
                result = food_vendor.customer_login()

        displayed_output = output.getvalue()

        assert result is None

        mismatch_count = displayed_output.count(
            "Username or password does not match."
        )

        assert mismatch_count == 2

        assert (
            "You have reached the maximum number of "
            "login attempts. Goodbye!"
            in displayed_output
        )

        print("PASS: Login stopped after three failed attempts.")
        print("PASS: Failed login returned None.")
        print("PASS: Maximum-attempt message was displayed.")
        print(
            "PASS: Mismatch message appeared only before "
            "attempts 2 and 3."
        )

        print()
        print("----------------------------------------")
        print("PHASE 11 CUSTOMER LOGIN PASSED!")
        print("----------------------------------------")

    finally:
        database.disconnect()
        print("PASS: Database disconnected.")


if __name__ == "__main__":
    test_customer_login()