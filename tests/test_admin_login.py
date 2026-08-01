from contextlib import redirect_stdout
from io import StringIO
from unittest.mock import patch

from DbManager import DbManager
from FoodVendor import FoodVendor
from Users import Admin


def test_admin_login():
    database = DbManager()
    food_vendor = FoodVendor()

    try:
        food_vendor.initialize(database)

        cursor = database.conn.cursor()

        # Find one valid administrator.
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

        # Find one customer so we can prove customers cannot
        # authenticate through the administrator login.
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

        # -----------------------------------------------------
        # TEST 1: VALID ADMIN LOGIN
        # -----------------------------------------------------

        with patch(
            "builtins.input",
            side_effect=[
                admin_user_name,
                admin_password
            ]
        ):
            result = food_vendor.admin_login()

        assert result is not None
        assert isinstance(result, Admin)
        assert result.user_name == admin_user_name
        assert result.account == "admin"
        assert result.password == admin_password
        assert result.db is database

        print("PASS: Valid credentials returned an Admin object.")

        # -----------------------------------------------------
        # TEST 2: FAILED ATTEMPT FOLLOWED BY SUCCESS
        # -----------------------------------------------------

        output = StringIO()

        with patch(
            "builtins.input",
            side_effect=[
                admin_user_name,
                "wrong_password",
                admin_user_name,
                admin_password
            ]
        ):
            with redirect_stdout(output):
                result = food_vendor.admin_login()

        displayed_output = output.getvalue()

        assert isinstance(result, Admin)
        assert result.user_name == admin_user_name

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
        print("PASS: A later valid attempt returned the Admin.")

        # -----------------------------------------------------
        # TEST 3: CUSTOMER CANNOT LOG IN AS ADMIN
        # -----------------------------------------------------

        output = StringIO()

        with patch(
            "builtins.input",
            side_effect=[
                customer_user_name,
                customer_password,
                admin_user_name,
                admin_password
            ]
        ):
            with redirect_stdout(output):
                result = food_vendor.admin_login()

        displayed_output = output.getvalue()

        assert isinstance(result, Admin)
        assert result.user_name == admin_user_name
        assert result.account == "admin"

        assert (
            "Username or password does not match."
            in displayed_output
        )

        print("PASS: Customer credentials were rejected.")
        print("PASS: Admin credentials worked on the next attempt.")

        # -----------------------------------------------------
        # TEST 4: MISSING USERNAME IS REJECTED
        # -----------------------------------------------------

        output = StringIO()

        with patch(
            "builtins.input",
            side_effect=[
                "not_a_real_admin",
                "not_a_real_password",
                admin_user_name,
                admin_password
            ]
        ):
            with redirect_stdout(output):
                result = food_vendor.admin_login()

        displayed_output = output.getvalue()

        assert isinstance(result, Admin)

        assert (
            "Username or password does not match."
            in displayed_output
        )

        print("PASS: Missing administrator account was rejected.")
        print("PASS: Login continued after the missing username.")

        # -----------------------------------------------------
        # TEST 5: THREE FAILED ATTEMPTS
        # -----------------------------------------------------

        output = StringIO()

        with patch(
            "builtins.input",
            side_effect=[
                admin_user_name,
                "wrong_password_1",
                admin_user_name,
                "wrong_password_2",
                admin_user_name,
                "wrong_password_3"
            ]
        ):
            with redirect_stdout(output):
                result = food_vendor.admin_login()

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
        print("PASS: Mismatch message appeared only before attempts 2 and 3.")

        print()
        print("-------------------------------------")
        print("PHASE 10 ADMIN LOGIN PASSED!")
        print("-------------------------------------")

    finally:
        database.disconnect()
        print("PASS: Database disconnected.")


if __name__ == "__main__":
    test_admin_login()
