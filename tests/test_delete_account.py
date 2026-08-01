from unittest.mock import patch

from DbManager import DbManager
from Users import Admin


def insert_test_customer(database, user_name):
    customer = (
        user_name,
        "customer",
        "Test",
        "Customer",
        f"{user_name}@example.com",
        "5551234567",
        "TestPassword123",
        "",
        "4111111111111111",
        "1229",
        "100 Test Street",
        0,
        0
    )

    database.insert_user(customer)


def test_delete_account():
    database = DbManager()

    try:
        database.connect()
        database.create_user_table("user.tsv")

        # Retrieve an existing administrator.
        cursor = database.conn.cursor()

        cursor.execute(
            """
            SELECT user_name
            FROM user
            WHERE account_type = 'admin'
            LIMIT 1
            """
        )

        row = cursor.fetchone()

        assert row is not None, "No administrator was found in user.tsv."

        admin = database.get_admin(row[0])

        assert admin is not None
        assert isinstance(admin, Admin)
        assert admin.db is database

        print("PASS: Existing Admin retrieved with database access.")

        # ---------------------------------------------------------
        # TEST 1: SUCCESSFULLY DELETE AN EXISTING ACCOUNT
        # ---------------------------------------------------------

        insert_test_customer(database, "delete_me")

        assert database.is_user_exist("delete_me")

        successful_delete_inputs = [
            "delete_me",
            "Y"
        ]

        with patch(
            "builtins.input",
            side_effect=successful_delete_inputs
        ):
            admin.delete_account(admin)

        assert not database.is_user_exist("delete_me")

        print("PASS: Existing account was deleted after Y confirmation.")

        # ---------------------------------------------------------
        # TEST 2: LOWERCASE Y CONFIRMATION
        # ---------------------------------------------------------

        insert_test_customer(database, "delete_lowercase")

        assert database.is_user_exist("delete_lowercase")

        lowercase_yes_inputs = [
            "delete_lowercase",
            "y"
        ]

        with patch(
            "builtins.input",
            side_effect=lowercase_yes_inputs
        ):
            admin.delete_account(admin)

        assert not database.is_user_exist("delete_lowercase")

        print("PASS: Lowercase y deleted the selected account.")

        # ---------------------------------------------------------
        # TEST 3: CHOOSING N PRESERVES THE ACCOUNT
        # ---------------------------------------------------------

        insert_test_customer(database, "keep_me")

        assert database.is_user_exist("keep_me")

        cancel_delete_inputs = [
            "keep_me",
            "N"
        ]

        with patch(
            "builtins.input",
            side_effect=cancel_delete_inputs
        ):
            admin.delete_account(admin)

        assert database.is_user_exist("keep_me")

        print("PASS: Account was preserved after N confirmation.")

        # ---------------------------------------------------------
        # TEST 4: LOWERCASE N PRESERVES THE ACCOUNT
        # ---------------------------------------------------------

        insert_test_customer(database, "keep_lowercase")

        assert database.is_user_exist("keep_lowercase")

        lowercase_no_inputs = [
            "keep_lowercase",
            "n"
        ]

        with patch(
            "builtins.input",
            side_effect=lowercase_no_inputs
        ):
            admin.delete_account(admin)

        assert database.is_user_exist("keep_lowercase")

        print("PASS: Lowercase n preserved the selected account.")

        # ---------------------------------------------------------
        # TEST 5: NONEXISTENT USERNAME REPROMPTS
        # ---------------------------------------------------------

        insert_test_customer(database, "valid_after_missing")

        nonexistent_user_inputs = [
            "not_a_real_user",
            "valid_after_missing",
            "Y"
        ]

        with patch(
            "builtins.input",
            side_effect=nonexistent_user_inputs
        ):
            admin.delete_account(admin)

        assert not database.is_user_exist("valid_after_missing")

        print("PASS: Nonexistent username was rejected.")
        print("PASS: Method reprompted and deleted a valid account.")

        # ---------------------------------------------------------
        # TEST 6: SELF-DELETION IS PREVENTED
        # ---------------------------------------------------------

        insert_test_customer(database, "valid_after_self")

        logged_in_admin_username = admin.user_name

        assert database.is_user_exist(logged_in_admin_username)

        self_delete_inputs = [
            logged_in_admin_username,
            "valid_after_self",
            "Y"
        ]

        with patch(
            "builtins.input",
            side_effect=self_delete_inputs
        ):
            admin.delete_account(admin)

        assert database.is_user_exist(logged_in_admin_username)
        assert not database.is_user_exist("valid_after_self")

        print("PASS: Logged-in Admin could not delete their own account.")
        print("PASS: Method reprompted after self-deletion attempt.")

        # ---------------------------------------------------------
        # TEST 7: INVALID CONFIRMATION REPROMPTS
        # ---------------------------------------------------------

        insert_test_customer(database, "invalid_confirmation")

        invalid_confirmation_inputs = [
            "invalid_confirmation",
            "maybe",
            "Y"
        ]

        with patch(
            "builtins.input",
            side_effect=invalid_confirmation_inputs
        ):
            admin.delete_account(admin)

        assert not database.is_user_exist("invalid_confirmation")

        print("PASS: Invalid confirmation response was rejected.")
        print("PASS: Valid replacement confirmation was accepted.")

        print()
        print("PHASE 7 ADMIN ACCOUNT DELETION PASSED!")

    finally:
        database.disconnect()
        print("PASS: Database disconnected.")


if __name__ == "__main__":
    test_delete_account()