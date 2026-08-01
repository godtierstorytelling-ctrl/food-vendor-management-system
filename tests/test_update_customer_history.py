from DbManager import DbManager

database = DbManager()

try:
    database.connect()
    database.create_user_table("user.tsv")

    cursor = database.conn.cursor()

    # Find a user with order history
    cursor.execute("""
        SELECT user_name, order_history
        FROM user
        WHERE order_history IS NOT NULL
        LIMIT 1
    """)

    user_name, original_history = cursor.fetchone()

    print(
        f"Before update: {user_name} has "
        f"order history value {original_history}."
    )
    
    # Save other users before update
    cursor.execute("""
        SELECT user_name, order_history
        FROM user
        WHERE user_name != ?
    """, (user_name,))

    other_users_before = cursor.fetchall()

    # Update selected user
    new_history_value = 9999

    database.update_customer_history(
        user_name,
        new_history_value
    )

    # Verify selected user changed
    cursor.execute("""
        SELECT order_history
        FROM user
        WHERE user_name = ?
    """, (user_name,))

    updated_history = cursor.fetchone()[0]

    assert updated_history == new_history_value

    print(
        f"PASS: {user_name} now has "
        f"order history value {updated_history}."
    )

    # Verify others stayed unchanged
    cursor.execute("""
        SELECT user_name, order_history
        FROM user
        WHERE user_name != ?
    """, (user_name,))

    other_users_after = cursor.fetchall()

    assert other_users_before == other_users_after 
    print("PASS: Other users were not changed.")

finally:
    database.disconnect()
    print("PASS: Database disconnected.")