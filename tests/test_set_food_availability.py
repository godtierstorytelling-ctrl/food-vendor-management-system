from DbManager import DbManager

database = DbManager()

try:
    database.connect()
    database.create_menu_table("menu.tsv")

    item_name = "Ham"
    category = "Sandwiches"

    # Confirm Ham starts as available
    assert database.is_food_available(item_name) is True

    print(f"PASS: {item_name} is initally available.")

    # Make Ham unavailable
    database.set_food_availability(
        item_name,
        0
    )

    # Verify using is_food_available
    assert database.is_food_available(item_name) is False

    print(f"PASS: {item_name} is now unavailable.")

    # Display the category to verify Ham is excluded
    print("\nSandwiches after making Ham unavailable:")
    print("----------------------------------------")

    database.display_daily_menu(category)

    # Make Ham available again
    database.set_food_availability(
        item_name,
        1
    )

    assert database.is_food_available(item_name) is True
    
    print(f"\nPASS: {item_name} is available again.")

    # Display again to verify Ham returns
    print("\nSandwiches after making Ham available:")
    print("--------------------------------------")

    database.display_daily_menu(category)

finally:
    database.disconnect()
    print("PASS: Database disconnected.")