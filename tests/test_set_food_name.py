from DbManager import DbManager

database = DbManager()

try:
    database.connect()
    database.create_menu_table("menu.tsv")

    old_name = "Ham"
    new_name = "Deluxe Ham Sandwich"

    cursor = database.conn.cursor()

    # Confirm the old name exists before the update
    cursor.execute("""
        SELECT item_name
        FROM menu
        WHERE item_name = ?
    """, (old_name,)
    )

    assert cursor.fetchone() is not None

    print(f"PASS: '{old_name}' exists before the update.")

    # Rename the item
    database.set_food_name(
        old_name,
        new_name
    )

    # Confirm the old name no longer exists
    cursor.execute("""
        SELECT item_name
        FROM menu
        WHERE item_name = ?
    """, (old_name,))

    assert cursor.fetchone() is None

    print(f"PASS: Old name '{old_name}' no longer exists.")

    # Confirm the new name exists
    cursor.execute("""
        SELECT item_name
        FROM menu
        WHERE item_name = ?
    """, (new_name,))

    assert cursor.fetchone() is not None

    print(f"PASS: New name '{new_name}' now exists.")

finally:
    database.disconnect()
    print("PASS: Database disconnected.")
    


