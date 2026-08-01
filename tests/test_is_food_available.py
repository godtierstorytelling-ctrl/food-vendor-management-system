from DbManager import DbManager

database = DbManager()

try:
    database.connect()
    database.create_menu_table("menu.tsv")

    item_name = "Ham"

    # Test an available item
    available_result = database.is_food_available(
        item_name
    )

    assert available_result is True
    assert isinstance(available_result, bool)

    print(
        f"PASS: Available item '{item_name}' "
        f"returned True."
    )

    # Make item unavailable
    database.set_food_availability(
        item_name,
        0
    )

    unavailable_result = database.is_food_available(
        item_name
    )

    assert unavailable_result is False
    assert isinstance(unavailable_result, bool)

    print(
        f"PASS: Unavailable item '{item_name}' "
        f"returned False."
    )

    # Test a nonexistent item
    missing_item = "Unicorn Taco Supreme"

    missing_result = database.is_food_available(
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
    print("PASS: Database disconnected.")
    