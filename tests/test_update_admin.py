from DbManager import DbManager
from Users import Admin

database = DbManager()

try:
    database.connect()
    database.create_user_table("user.tsv")

    # Find an existing admin username directly from the test database
    cursor = database.conn.cursor()

    cursor.execute("""
        SELECT user_name
        FROM user
        WHERE account_type = 'admin'
        LIMIT 1
    """)

    result = cursor.fetchone()

    assert result is not None, "No admin account was found in user.tsv."

    admin_username = result[0]

    # Test get_admin().
    admin = database.get_admin(admin_username)

    assert admin is not None
    assert isinstance(admin, Admin)
    assert admin.user_name == admin_username

    print("PASS: Admin was retrieved successfully.")
    print(f"Admin: {admin}")
    print(f"Before update: {admin.phone_num}, {admin.email}")

    # Preserve unrelated values so we can confirm they do not change.
    original_first_name = admin.first_name
    original_last_name = admin.last_name
    original_password = admin.password
    original_employee_id = admin.employ_id

    # Change the Admin object's phone number and email.
    admin.phone_num = "555-999-0000"
    admin.email = "updated_admin@example.com"

    # Write those changes to this database.
    database.update_admin(admin)

    # Retrieve a fresh Admin object from the database.
    updated_admin = database.get_admin(admin_username)

    assert updated_admin is not None
    assert updated_admin.phone_num == "555-999-0000"
    assert updated_admin.email == "updated_admin@example.com"

    print("PASS: Admin phone number was updated.")
    print("PASS: Admin email was updated.")

    # Confirm unrelated fields were not changed.
    assert updated_admin.first_name == original_first_name
    assert updated_admin.last_name == original_last_name
    assert updated_admin.password == original_password
    assert updated_admin.employ_id == original_employee_id

    print("PASS: Unrelated Admin fields were not changed.")
    print(
        f"After update: "
        f"{updated_admin.phone_num}, {updated_admin.email}"
    )

    # Test a username that does not exist.

    missing_admin = database.get_admin("not_a_real_admin")

    assert missing_admin is None

    print("PASS: get_admin() returns None for an unknown admin.")
    print("PHASE 4 ADMIN METHODS PASSED!")

finally:
    database.disconnect()
    print("PASS: Database disconnected.")