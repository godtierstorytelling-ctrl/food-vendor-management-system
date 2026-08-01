from DbManager import DbManager

database = DbManager()

try:
    database.connect()
    database.create_menu_table("menu.tsv")

    item_name = "Ham"
    new_category = "Specials"

    # Update the item's category
    database.set_food_category(
        item_name,
        new_category
    )

    # Verify the category directly
    cursor = database.conn.cursor()

    cursor.execute("""
        SELECT category
        FROM menu
        WHERE item_name = ?
    """, (item_name,))

    updated_category = cursor.fetchone()[0]

    assert updated_category == new_category
    
    print(
        f"PASS: {item_name} was moved to "
        f"the {updated_category} category."
    )

    # Confirm it appears when displaying the new category
    print("\nDisplaying nw category:")
    print("----------------------")

    database.display_daily_menu(new_category)

finally:
    database.disconnect()
    print("PASS: Database disconnect.")
    