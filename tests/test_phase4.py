from DbManager import DbManager

database = DbManager()

try:
    # ARRANGE
    database.connect()
    database.create_user_table("user.tsv")

    test_user = (
        "phase4_test_user",
        "customer",
        "Test",
        "User",
        "testuser@example.com",
        "5551234567",
        "password123",
        "",
        "1234567890123456",
        "1228",
        "123 Test Street",
        10,
        100
    )

    # ACT + ASSERT 1: Insert user
    database.insert_user(test_user)

    assert database.is_user_exist("phase4_test_user") is True
    print("PASS: Test user was inserted.")

    # ACT + ASSERT 2: Update rewards
    database.update_customer_rewards(
        "phase4_test_user",
        500
    )

    cursor = database.conn.cursor()

    cursor.execute("""
        SELECT reward_points
        FROM user
        WHERE user_name = ?
    """, ("phase4_test_user",))

    reward_points = cursor.fetchone()[0]

    assert reward_points == 500
    print("PASS: Reward points were updated.")

    # ACT + ASSERT 3: Update order history
    database.update_customer_history(
        "phase4_test_user",
        9999
    )

    cursor.execute("""
        SELECT order_history
        FROM user
        WHERE user_name = ?
    """, ("phase4_test_user",))

    order_history = cursor.fetchone()[0]

    assert order_history == 9999
    print("PASS: Order history was updated.")

    # ASSERT 4: User still exists after updates
    assert database.is_user_exist("phase4_test_user") is True
    print("PASS: Test user still exists after updates.")

    # ACT + ASSERT 5: Delete user
    database.delete_user("phase4_test_user")

    assert database.is_user_exist("phase4_test_user") is False
    print("PASS: Test user was deleted.")

    print("\nPHASE 4 PASSED!")

finally:
    database.disconnect()
    print("PASS: Database disconnected.")