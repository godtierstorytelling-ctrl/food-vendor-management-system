from DbManager import DbManager

database = DbManager()

try:
    # ARRANGE
    database.connect()
    database.create_menu_table("menu.tsv")

    original_name = "Ham"
    new_name = "Deluxe Ham Sandwich"
    original_category = "Sandwiches"
    new_category = "Specials"

    # Verify starting state
    assert database.is_food_exist(original_name) is True
    assert database.is_food_available(original_name) is True

    original_price = database.get_food_price(original_name)
    original_time = database.get_food_time(original_name)

    assert original_price != -1.0
    assert original_time != -1

    print("PASS: Original menu item exists and is available.")
    print(
        f"PASS: Original price is ${original_price:.2f} "
        f"and prep time is {original_time} minutes."
    )

    # UPDATE PRICE
    database.set_food_price(
        original_name,
        19.99
    )

    assert database.get_food_price(original_name) == 19.99
    print("PASS: Food price was updated.")

    # UPDATE CATEGORY
    database.set_food_category(
        original_name,
        new_category
    )

    cursor = database.conn.cursor()

    cursor.execute("""
        SELECT category
        FROM menu
        WHERE item_name = ?
    """, (original_name,))

    assert cursor.fetchone()[0] == new_category

    print("PASS: Food category was updated.")

    # UPDATE DESCRIPTION
    new_description = (
        "Freshly sliced ham on artisan bread"
    )

    database.set_food_description(
        original_name,
        new_description
    )

    cursor.execute("""
        SELECT description
        FROM menu
        WHERE item_name = ?
    """, (original_name,))

    assert cursor.fetchone()[0] == new_description
    print("PASS: Food description was updated.")

    # MAKE ITEM UNAVAILABLE
    database.set_food_availability(
        original_name,
        0
    )

    assert database.is_food_available(original_name) is False
    print("PASS: Food availability was updated to unavailable.")

    # MAKE ITEM AVAILABLE AGAIN
    database.set_food_availability(
        original_name,
        1
    )

    assert database.is_food_available(original_name) is True
    print("PASS: Food availability was restored.")

    #RENAME ITEM
    database.set_food_name(
        original_name,
        new_name
    )

    assert database.is_food_exist(original_name) is False
    assert database.is_food_exist(new_name) is True

    print("PASS: Food item was renamed.")

    # VERIFY DATA SURVIVED THE RENAME
    assert database.get_food_price(new_name) == 19.99
    assert database.get_food_time(new_name) == original_time
    assert database.is_food_available(new_name) is True

    print("PASS: Updated item data survived the rename.")

    # DISPLAY FINAL CATEGORY
    print("\nFinal Specials Menu:")
    print("--------------------")

    database.display_daily_menu(new_category)

    print("\nPHASE 5 PASSED!")

finally:
    database.disconnect()
    print("PASS: Database disconnected.")