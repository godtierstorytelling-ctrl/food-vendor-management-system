from unittest.mock import patch

from DbManager import DbManager
from Users import Customer


def test_update_customer_profile():
    database = DbManager()

    try:
        database.connect()
        database.create_user_table("user.tsv")

        cursor = database.conn.cursor()

        cursor.execute(
            """
            SELECT user_name
            FROM user
            WHERE account_type = 'customer'
            LIMIT 1
            """
        )

        row = cursor.fetchone()

        assert row is not None, "No customer was found in user.tsv."

        customer = database.get_customer(row[0])

        assert customer is not None
        assert isinstance(customer, Customer)
        assert customer.db is database

        print("PASS: Existing Customer retrieved with database access.")

        original_points = customer.points
        original_history = customer.history

        updated_card_num = "5555444433332222"
        updated_card_date = "1230"
        updated_address = "500 Phase Nine Avenue"
        updated_phone_num = "5559998888"
        updated_email = "phase9@example.com"

        profile_inputs = [
            updated_card_num,
            updated_card_date,
            updated_address,
            updated_phone_num,
            updated_email
        ]

        with patch(
            "builtins.input",
            side_effect=profile_inputs
        ):
            customer.update_customer_profile(customer)

        # Verify the in-memory Customer object changed.
        assert customer.card_num == updated_card_num
        assert customer.card_date == updated_card_date
        assert customer.address == updated_address
        assert customer.phone_num == updated_phone_num
        assert customer.email == updated_email

        print("PASS: Customer object profile fields were updated.")

        # Verify protected values remained unchanged in memory.
        assert customer.points == original_points
        assert customer.history == original_history

        print("PASS: Customer points and history remained unchanged in memory.")

        # Retrieve a fresh Customer object from the database.
        updated_customer = database.get_customer(customer.user_name)

        assert updated_customer is not None

        # Verify the changes persisted.
        assert updated_customer.card_num == updated_card_num
        assert updated_customer.card_date == updated_card_date
        assert updated_customer.address == updated_address
        assert updated_customer.phone_num == updated_phone_num
        assert updated_customer.email == updated_email

        print("PASS: Updated profile persisted in the database.")

        # Verify points and history remained unchanged in the database.
        assert updated_customer.points == original_points
        assert updated_customer.history == original_history

        print("PASS: Database preserved customer points and history.")

        # Verify unrelated identity fields were not modified.
        assert updated_customer.user_name == customer.user_name
        assert updated_customer.account == customer.account
        assert updated_customer.first_name == customer.first_name
        assert updated_customer.last_name == customer.last_name
        assert updated_customer.password == customer.password

        print("PASS: Unrelated customer fields remained unchanged.")

        print()
        print("---------------------------------------------")
        print("PHASE 9 CUSTOMER PROFILE UPDATE PASSED!")
        print("---------------------------------------------")

    finally:
        database.disconnect()
        print("PASS: Database disconnected.")


if __name__ == "__main__":
    test_update_customer_profile()