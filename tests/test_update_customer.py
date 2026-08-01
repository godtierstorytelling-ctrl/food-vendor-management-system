from DbManager import DbManager
from Users import Customer

database = DbManager()

try:
    database.connect()
    database.create_user_table("user.tsv")

    # Find an existing customer username.
    cursor = database.conn.cursor()

    cursor.execute("""
        SELECT user_name
        FROM user
        WHERE account_type = 'customer'
        LIMIT 1
    """)

    result = cursor.fetchone()

    assert result is not None, "No customer account was found in user.tsv."

    customer_username = result[0]

    # Test get_customer().
    customer = database.get_customer(customer_username)

    assert isinstance(customer, Customer)
    assert customer.user_name == customer_username

    print("PASS: Customer was retrieved successfully.")
    print(f"Customer: {customer}")
    print(
        "Before update:",
        customer.card_num, 
        customer.card_date,
        customer.address,
        customer.phone_num, 
        customer.email
    )

    # Preserve fields that should not change.
    original_password = customer.password
    original_points = customer.points
    original_history = customer.history
    original_first_name = customer.first_name
    original_last_name = customer.last_name

    # Change editable profile fields.
    customer.card_num = "5555444433332222"
    customer.card_date = "12/30"
    customer.address = "100 Updated Avenue"
    customer.phone_num = "555-888-7777"
    customer.email = "updated_customer@example.com"

    # Save the changes.
    database.update_customer(customer)

    # Retrieve a fresh Customer object.
    updated_customer = database.get_customer(customer_username)

    assert updated_customer.card_num == "5555444433332222"
    assert updated_customer.card_date == "12/30"
    assert updated_customer.address == "100 Updated Avenue"
    assert updated_customer.phone_num == "555-888-7777"
    assert updated_customer.email == "updated_customer@example.com"

    print("PASS: Customer credit card number was updated.")
    print("PASS: Customer expiration date was updated.")
    print("PASS: Customer billing address was updated.")
    print("PASS: Customer phone number was updated.")
    print("PASS: Customer email was updated.")

    # Confirm protected and unrelated fields did not change.
    assert updated_customer.password == original_password
    assert updated_customer.points == original_points
    assert updated_customer.history == original_history
    assert updated_customer.first_name == original_first_name
    assert updated_customer.last_name == original_last_name

    print("PASS: Password, points, and history were not changed.")
    print("PASS: Unrelated Customer fields were not changed.")

    print(
        "After update:",
        updated_customer.card_num,
        updated_customer.card_date,
        updated_customer.address,
        updated_customer.phone_num,
        updated_customer.email
    )

    # Test the assignment-specific missing-customer behavior.
    missing_customer = database.get_customer("not_a_real_customer")

    assert isinstance(missing_customer, Customer)
    assert missing_customer.user_name == ""
    assert missing_customer.account == ""
    assert missing_customer.first_name == ""
    assert missing_customer.last_name == ""
    assert missing_customer.email == ""
    assert missing_customer.phone_num == ""
    assert missing_customer.password == ""
    assert missing_customer.card_num == ""
    assert missing_customer.card_date == ""
    assert missing_customer.address == ""
    assert missing_customer.points == 0
    assert missing_customer.history == 0

    # Confirm numeric defaults are integers.
    assert isinstance(missing_customer.points, int)
    assert isinstance(missing_customer.history, int)

    print("PASS: Missing customer returns an empty Customer object.")
    print("PASS: Missing Customer numeric defaults are integers.")
    print("PHASE 4 CUSTOMER METHODS PASSED!")

finally:
    database.disconnect()
    print("PASS: Database disconnected.")