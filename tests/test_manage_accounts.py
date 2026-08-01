from unittest.mock import patch

from DbManager import DbManager
from Users import Admin


def test_manage_accounts():
    database = DbManager()

    try:
        database.connect()
        database.create_user_table("user.tsv")

        cursor = database.conn.cursor()

        cursor.execute("""
            SELECT user_name
            FROM user
            WHERE account_type='admin'
            LIMIT 1
        """)

        row = cursor.fetchone()

        assert row is not None

        admin = database.get_admin(row[0])

        assert isinstance(admin, Admin)

        print("PASS: Admin successfully retrieved.")

        # ---------------------------------------------------
        # OPTION 5
        # Return immediately
        # ---------------------------------------------------

        print()
        print("Testing Option 5...")

        with patch(
            "builtins.input",
            side_effect=["5"]
        ):
            admin.manage_accounts(admin)

        print("PASS: Option 5 returned correctly.")

        # ---------------------------------------------------
        # OPTION 1
        # Update Admin Profile
        # ---------------------------------------------------

        print()
        print("Testing Option 1...")

        with patch(
            "builtins.input",
            side_effect=[
                "1",
                "5558889999",
                "phase8@example.com",
                "5"
            ]
        ):
            admin.manage_accounts(admin)

        updated_admin = database.get_admin(admin.user_name)

        assert updated_admin.phone_num == "5558889999"
        assert updated_admin.email == "phase8@example.com"

        print("PASS: Option 1 called update_admin_profile().")

        # ---------------------------------------------------
        # OPTION 3
        # Create Account
        # ---------------------------------------------------

        print()
        print("Testing Option 3...")

        with patch(
            "builtins.input",
            side_effect=[
                "3",

                "phase8customer",
                "Password123",
                "Y",

                "Phase",
                "Eight",

                "phase8@example.com",
                "5554443333",

                "4111111111111111",
                "0929",
                "100 Test Street",

                "5"
            ]
        ):
            admin.manage_accounts(admin)

        assert database.is_user_exist("phase8customer")

        print("PASS: Option 3 called create_account().")

        # ---------------------------------------------------
        # OPTION 4
        # Delete Account
        # ---------------------------------------------------

        print()
        print("Testing Option 4...")

        with patch(
            "builtins.input",
            side_effect=[
                "4",
                "phase8customer",
                "Y",
                "5"
            ]
        ):
            admin.manage_accounts(admin)

        assert not database.is_user_exist("phase8customer")

        print("PASS: Option 4 called delete_account().")

        print()
        print("-------------------------------------")
        print("PHASE 8 MANAGE ACCOUNTS PASSED!")
        print("-------------------------------------")

    finally:
        database.disconnect()

        print("PASS: Database disconnected.")


if __name__ == "__main__":
    test_manage_accounts()