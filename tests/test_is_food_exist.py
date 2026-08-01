from DbManager import DbManager

database = DbManager()

try:
    database.connect()
    database.create_menu_table("menu.tsv")

    # Test an existing item
    existing_item = "Ham"

    existing_result = database.is_food_exist(
        existing_item
    )

    assert existing_result is True
    assert isinstance(existing_result, bool)

    print(
        f"PASS: Existing item '{existing_item}' "
        f"returned True."
    )

    # Test a nonexistent item
    missing_item = "Unicorn Taco Surpreme"

    missing_result = database.is_food_exist(
        missing_item
    )

    assert missing_result is False
    assert isinstance(missing_result, bool)

    print(
        f"PASS: Nonexistent item '{missing_item}' "
        f"returned False."
    )

finally:
    database.disconnect()
    print("PASS: Databse disconnected.")