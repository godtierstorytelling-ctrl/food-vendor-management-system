from DbManager import DbManager

database = DbManager()

try:
    database.connect()
    database.create_menu_table("menu.tsv")

    print("TEST: Sandwiches")
    print("----------------")

    database.display_daily_menu("Sandwiches")

finally:
    database.disconnect()
    