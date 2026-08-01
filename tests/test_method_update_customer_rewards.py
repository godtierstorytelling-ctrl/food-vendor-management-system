from DbManager import DbManager

database = DbManager()

try:
    database.connect()
    database.create_user_table("user.tsv")

    cursor = database.conn.cursor()

    # Pick one known user
    cursor.execute("""
        SELECT user_name, reward_points
        FROM user
        WHERE reward_points IS NOT NULL
        LIMIT 1
    """)

    user_name, original_rewards = cursor.fetchone()

    print(
        f"Before update: {user_name} has {original_rewards} reward points."
    )

    # Count how many other users have a specific value before the update

    cursor.execute("""
        SELECT user_name, reward_points
        FROM user
        WHERE user_name != ?
    """, (user_name,))

    other_users_before = cursor.fetchall()

    # Update the selected customer
    new_reward_value = 999

    database.update_customer_rewards(
        user_name, 
        new_reward_value
    )

    # Confirm selected user changed
    cursor.execute("""
        SELECT reward_points
        FROM user
        WHERE user_name = ?
    """, (user_name,))

    updated_rewards = cursor.fetchone()[0]

    assert updated_rewards == new_reward_value

    print(
        f"PASS: {user_name} now has "
        f"{updated_rewards} reward points."
    )

    # Confirm other users did not change
    cursor.execute("""
        SELECT user_name, reward_points
        FROM user
        WHERE user_name != ?
    """, (user_name,))

    other_users_after = cursor.fetchall()

    assert other_users_before == other_users_after

    print("PASS: Other users were not changed.")

finally:
    database.disconnect()
    print("PASS: Database disconnected.")