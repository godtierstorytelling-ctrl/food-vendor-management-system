from DbManager import DbManager

database = DbManager()

try:
    database.connect()
    database.create_user_table("user.tsv")

    # Find a known username from the database

    cursor = database.conn.cursor()

    cursor.execute("""
        SELECT user_name
        FROM user
        LIMIT 1
    """)

    existing_user = cursor.fetchone()[0]

    # Test an existing username
    result = database.is_user_exist(existing_user)

    assert result is True
    assert isinstance(result, bool)

    print(
        f"PASS: Existing username '{existing_user}' "
        f"returned True."
    )

    # Test a username that does not exist
    fake_user = "definitely_not_a_real_user_12345"

    result = database.is_user_exist(fake_user)

    assert result is False
    assert isinstance(result, bool)

    print(
        f"PASS: Nonexistent username '{fake_user}' "
        f"returned False."
    )

    # Test capitalization behavior
    changed_case = existing_user.swapcase()

    result = database.is_user_exist(changed_case)

    print(
        f"Capitalization test: '{changed_case}' "
        f"returned {result}."
    )

    assert result is False

    print("PASS: Username matching is case-sensitive.")

finally:
    database.disconnect()
    print("PASS: Database disconnected.")