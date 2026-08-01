from DbManager import DbManager

database = DbManager()

try:
    database.connect()
    database.create_menu_table("menu.tsv")

    # Test an existing item
    existing_item = "Ham"

    price = database.get_food_price(existing_item)

    assert price == 13.20
    assert isinstance(price, float)

    print(
        f"PASS: {existing_item} costs ${price:.2f}."
    )

    print(
        f"PASS: Existing item returned type "
        f"{type(price).__name__}."
    )

    # Test a nonexistent item
    missing_item = "Unicorn Taco Supreme"

    missing_price = database.get_food_price(
        missing_item
    )

    assert missing_price == -1.0
    assert isinstance(missing_price, float)

    print(
        f"PASS: Nonexistent item returned "
        f"{missing_price}."
    )

    print(
        "PASS: Missing-item result is exactly -1.0."
    )

finally:
    database.disconnect()
    print("PASS: Database disconnected.")
    