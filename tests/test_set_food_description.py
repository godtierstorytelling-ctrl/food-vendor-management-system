from DbManager import DbManager

database = DbManager()

try:
    database.connect()
    database.create_menu_table("menu.tsv")

    item_name = "Ham"
    new_description = "Freshly sliced ham on artisan bread"

    # Udpate the description
    database.set_food_description(
        item_name,
        new_description
    )

    # Verify the updated description
    cursor = database.conn.cursor()

    cursor.execute("""
        SELECT description
        FROM menu
        WHERE item_name = ?
    """, (item_name,))

    updated_description = cursor.fetchone()[0]

    assert updated_description == new_description
    print(
        f"PASS: {item_name} description was updated."
    )

    print(
        f"New description: {updated_description}"
    )

finally:
    database.disconnect()
    print("PASS: Database disconnected.")