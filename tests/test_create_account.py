from unittest.mock import patch

from DbManager import DbManager
from Users import Admin


def get_database_row(database, user_name):
    cursor = database.conn.cursor()

    cursor.execute(
        """
        SELECT
            user_name,
            account_type,
            first_name,
            last_name,
            email,
            phone_number,
            password,
            employee_id,
            credit_card_number,
            credit_card_exp_date,
            billing_address,
            reward_points,
            order_history
        FROM user
        WHERE user_name = ?
        """,
        (user_name,)
    )

    return cursor.fetchone()


def test_create_account():
    database = DbManager()

    try:
        database.connect()
        database.create_user_table("user.tsv")

        # Retrieve an existing administrator to perform account creation.
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
        # TEST 1: CREATE A NEW ADMIN ACCOUNT
        # ---------------------------------------------------------

        new_admin_inputs = [
            "phase6admin",
            "AdminPassword123",
            "N",
            "Phase",
            "SixAdmin",
            "phase6admin@example.com",
            "5551112222",
            "FV9001"
        ]

        with patch("builtins.input", side_effect=new_admin_inputs):
            admin.create_account()

        assert database.is_user_exist("phase6admin")

        print("PASS: New Admin username exists in the database.")

        new_admin_row = get_database_row(
            database,
            "phase6admin"
        )

        assert new_admin_row is not None

        assert new_admin_row[0] == "phase6admin"
        assert new_admin_row[1] == "admin"
        assert new_admin_row[2] == "Phase"
        assert new_admin_row[3] == "SixAdmin"
        assert new_admin_row[4] == "phase6admin@example.com"
        assert new_admin_row[5] == "5551112222"
        assert new_admin_row[6] == "AdminPassword123"
        assert new_admin_row[7] == "FV9001"

        # Customer-only fields should be safely empty/defaulted.
        assert new_admin_row[8] == ""
        assert new_admin_row[9] == ""
        assert new_admin_row[10] == ""
        assert new_admin_row[11] is None
        assert new_admin_row[12] is None

        print("PASS: Admin account fields were stored correctly.")
        print("PASS: Admin customer-only fields were stored safely.")

        # Confirm the new row can be converted back into an Admin object.
        created_admin = database.get_admin("phase6admin")

        assert created_admin is not None
        assert isinstance(created_admin, Admin)
        assert created_admin.user_name == "phase6admin"
        assert created_admin.employ_id == "FV9001"

        print("PASS: New Admin can be retrieved as an Admin object.")

        # ---------------------------------------------------------
        # TEST 2: CREATE A NEW CUSTOMER ACCOUNT
        # ---------------------------------------------------------

        new_customer_inputs = [
            "phase6customer",
            "CustomerPassword123",
            "y",
            "Phase",
            "SixCustomer",
            "phase6customer@example.com",
            "5553334444",
            "4111111111111111",
            "0929",
            "600 Python Way, Code City, NY 10001"
        ]

        with patch("builtins.input", side_effect=new_customer_inputs):
            admin.create_account()

        assert database.is_user_exist("phase6customer")

        print("PASS: New Customer username exists in the database.")

        new_customer_row = get_database_row(
            database,
            "phase6customer"
        )

        assert new_customer_row is not None

        assert new_customer_row[0] == "phase6customer"
        assert new_customer_row[1] == "customer"
        assert new_customer_row[2] == "Phase"
        assert new_customer_row[3] == "SixCustomer"
        assert new_customer_row[4] == "phase6customer@example.com"
        assert new_customer_row[5] == "5553334444"
        assert new_customer_row[6] == "CustomerPassword123"

        # Admin-only field should be safely empty.
        assert new_customer_row[7] == ""

        assert new_customer_row[8] == "4111111111111111"
        assert new_customer_row[9] == "0929"
        assert (
            new_customer_row[10]
            == "600 Python Way, Code City, NY 10001"
        )
        assert new_customer_row[11] == 0
        assert new_customer_row[12] == 0

        print("PASS: Customer account fields were stored correctly.")
        print("PASS: Customer Admin-only field was stored safely.")
        print("PASS: Customer rewards and history defaulted to zero.")

        # Confirm the new row can be converted back into a Customer object.
        created_customer = database.get_customer(
            "phase6customer"
        )

        assert created_customer.user_name == "phase6customer"
        assert created_customer.account == "customer"
        assert created_customer.card_num == "4111111111111111"
        assert created_customer.card_date == "0929"
        assert (
            created_customer.address
            == "600 Python Way, Code City, NY 10001"
        )
        assert created_customer.points == 0
        assert created_customer.history == 0

        print(
            "PASS: New Customer can be retrieved "
            "as a Customer object."
        )

        # ---------------------------------------------------------
        # TEST 3: DUPLICATE USERNAME VALIDATION
        # ---------------------------------------------------------

        duplicate_username_inputs = [
            "phase6admin",
            "phase6admin2",
            "SecondAdminPassword",
            "n",
            "Second",
            "Administrator",
            "phase6admin2@example.com",
            "5557778888",
            "FV9002"
        ]

        with patch(
            "builtins.input",
            side_effect=duplicate_username_inputs
        ):
            admin.create_account()

        assert database.is_user_exist("phase6admin2")

        duplicate_test_row = get_database_row(
            database,
            "phase6admin2"
        )

        assert duplicate_test_row is not None
        assert duplicate_test_row[0] == "phase6admin2"
        assert duplicate_test_row[1] == "admin"
        assert duplicate_test_row[7] == "FV9002"

        print("PASS: Existing username was rejected.")
        print("PASS: Available replacement username was accepted.")

        # Confirm the original account was not overwritten.
        original_admin_row = get_database_row(
            database,
            "phase6admin"
        )

        assert original_admin_row[6] == "AdminPassword123"
        assert original_admin_row[7] == "FV9001"

        print("PASS: Existing account was not overwritten.")

        # ---------------------------------------------------------
        # TEST 4: RESERVED GUEST USERNAME
        # ---------------------------------------------------------

        guest_username_inputs = [
            "Guest",
            "phase6customer2",
            "SecondCustomerPassword",
            "Y",
            "Second",
            "Customer",
            "phase6customer2@example.com",
            "5559990000",
            "5555555555554444",
            "1230",
            "700 Database Drive, Query Town, NY 10002"
        ]

        with patch(
            "builtins.input",
            side_effect=guest_username_inputs
        ):
            admin.create_account()

        assert database.is_user_exist("phase6customer2")

        guest_test_row = get_database_row(
            database,
            "phase6customer2"
        )

        assert guest_test_row is not None
        assert guest_test_row[1] == "customer"

        print("PASS: Reserved Guest username was rejected.")
        print("PASS: Replacement customer account was created.")

        # ---------------------------------------------------------
        # TEST 5: INVALID ACCOUNT-TYPE INPUT
        # ---------------------------------------------------------

        invalid_choice_inputs = [
            "phase6admin3",
            "ThirdAdminPassword",
            "maybe",
            "N",
            "Third",
            "Administrator",
            "phase6admin3@example.com",
            "5552221111",
            "FV9003"
        ]

        with patch(
            "builtins.input",
            side_effect=invalid_choice_inputs
        ):
            admin.create_account()

        invalid_choice_row = get_database_row(
            database,
            "phase6admin3"
        )

        assert invalid_choice_row is not None
        assert invalid_choice_row[1] == "admin"
        assert invalid_choice_row[7] == "FV9003"

        print("PASS: Invalid account-type input was rejected.")
        print("PASS: Valid replacement choice was accepted.")

        print()
        print("PHASE 6 ADMIN ACCOUNT CREATION PASSED!")

    finally:
        database.disconnect()
        print("PASS: Database disconnected.")


if __name__ == "__main__":
    test_create_account()
