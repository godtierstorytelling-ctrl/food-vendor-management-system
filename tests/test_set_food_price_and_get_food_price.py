from DbManager import DbManager

database = DbManager()

try:
    database.connect()
    database.create_menu_table("menu.tsv")

    # Choose a known menu item
    item_name = "Ham"

    original_price = database.get_food_price(item_name)

    print(
        f"Before update: {item_name} costs "
        f"${original_price:.2f}."
    )

    # Update the price
    new_price = 19.99

    database.set_food_price(
        item_name,
        new_price
    )

    # Verify using get_food_price()
    updated_price = database.get_food_price(item_name)

    assert updated_price == new_price

    print(
        f"PASS: {item_name} now costs "
        f"${updated_price:.2f}."
    )

finally:
    database.disconnect()
    print("PASS: Database disconnected.")
