from DbManager import DbManager

database = DbManager()

try:
    database.connect()
    database.create_menu_table("menu.tsv")

    # Test an existing item
    existing_item = "Ham"

    prep_time = database.get_food_time(existing_item)

    assert prep_time != -1
    assert isinstance(prep_time, int)

    print(
        f"PASS: {existing_item} has a preparation "
        f"time of {prep_time} minutes."
    )

    # Test a nonexistent item
    missing_item = "Unicorn Taco Supreme"

    missing_time = database.get_food_time(
        missing_item
    )

    assert missing_time == -1

    print(
        f"PASS: Nonexistent item returned {missing_time}."
    )

    print(
        "PASS: Missing-item result is exactly -1."
    )

finally:
    database.disconnect()
    print("PASS: Database disconnected.")
