from DbManager import DbManager

database = DbManager()

try:
    database.connect()
    database.create_user_table("user.tsv")

    cursor = database.conn.cursor()

    # Choose a known user
    cursor.execute("""
        SELECT user_name
        FROM user
        LIMIT 1
    """)

    user_name = cursor.fetchone()[0]

    # Confirm user exists before deletion
    assert database.is_user_exist(user_name) is True

    print(
        f"PASS: '{user_name}' exists before deletion."
    )

    # Count all users before deletion

    cursor.execute("SELECT COUNT(*) FROM user")
    count_before = cursor.fetchone()[0]

    # Delete the selected user 
    database.delete_user(user_name)

    # Confirm the deleted user no longer exists
    assert database.is_user_exist(user_name) is False

    print(
        f"PASS: '{user_name}' no longer exists after deletion."
    )

    # Count all users after deletion
    cursor.execute("SELECT COUNT(*) FROM user")
    count_after = cursor.fetchone()[0]

    # Exactly one user should have been deleted
    assert count_after == count_before - 1

    print("PASS: Exactly one user was deleted.")

finally:
    database.disconnect()
    print("PASS: Database disconnected.")
