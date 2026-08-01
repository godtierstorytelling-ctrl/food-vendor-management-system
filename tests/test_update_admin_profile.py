from unittest.mock import patch

from DbManager import DbManager
from Users import Admin


def test_update_admin_profile():
    database = DbManager()

    try:
        database.connect()
        database.create_user_table("user.tsv")

        # Find one administrator in the database.
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

        admin_username = row[0]

        # Retrieve the administrator as an Admin object.
        admin = database.get_admin(admin_username)

        assert admin is not None
        assert isinstance(admin, Admin)
        assert admin.db is database

        print("PASS: Admin was retrieved with database access.")
        print(f"Before update: {admin.phone_num}, {admin.email}")

        # Simulate the user entering a new phone number and email address.
        simulated_inputs = [
            "5552223333",
            "phase5_admin@example.com"
        ]

        with patch("builtins.input", side_effect=simulated_inputs):
            admin.update_admin_profile(admin)

        # Confirm the current Admin object was updated.
        assert admin.phone_num == "5552223333"
        assert admin.email == "phase5_admin@example.com"

        print("PASS: Admin object was updated.")

        # Retrieve a fresh Admin object to confirm database persistence.
        updated_admin = database.get_admin(admin_username)

        assert updated_admin is not None
        assert updated_admin.phone_num == "5552223333"
        assert updated_admin.email == "phase5_admin@example.com"

        print("PASS: Admin phone number persisted in the database.")
        print("PASS: Admin email persisted in the database.")
        print(
            f"After update: "
            f"{updated_admin.phone_num}, {updated_admin.email}"
        )

        # Confirm unrelated Admin fields did not change.
        assert updated_admin.user_name == admin_username
        assert updated_admin.account == admin.account
        assert updated_admin.first_name == admin.first_name
        assert updated_admin.last_name == admin.last_name
        assert updated_admin.password == admin.password
        assert updated_admin.employ_id == admin.employ_id

        print("PASS: Unrelated Admin fields were not changed.")
        print("PHASE 5 ADMIN PROFILE MANAGEMENT PASSED!")

    finally:
        database.disconnect()
        print("PASS: Database disconnected.")


if __name__ == "__main__":
    test_update_admin_profile()