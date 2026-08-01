from DbManager import DbManager
database = DbManager()

try:
    # Test connection

    database.connect()
    assert database.conn is not None
    print("PASS: Database connection established.")

    # Test menu table creation and loading
    database.create_menu_table("menu.tsv")

    cursor = database.conn.cursor()

    cursor.execute("""
        SELECT name
        FROM sqlite_master
        WHERE type = 'table' AND name = 'menu'
    """)

    assert cursor.fetchone() is not None
    print("PASS: Menu table exists.")

    cursor.execute("SELECT COUNT(*) FROM menu")
    menu_count = cursor.fetchone()[0]

    assert menu_count > 0
    print(f"PASS: Menu table contains {menu_count} records.")

    # Test user table creation and loading
    database.create_user_table("user.tsv")

    cursor.execute("""
        SELECT name
        FROM sqlite_master
        WHERE type = 'table' AND name = 'user'
    """)

    assert cursor.fetchone() is not None
    print("PASS: User table exists.")

    cursor.execute("SELECT COUNT(*) FROM user")
    user_count = cursor.fetchone()[0]

    assert user_count > 0
    print(f"PASS: User table contains {user_count} records.")

    # Check numeric fields
    cursor.execute("""
        SELECT price, prep_time, available
        FROM menu
        LIMIT 1
    """)

    price, prep_time, available = cursor.fetchone()

    assert isinstance(price, float)
    assert isinstance(prep_time, int)
    assert isinstance(available, int)

    print("PASS: Menu numeric fields use the expected Python types.")

    # Check generated IDs
    cursor.execute("SELECT id FROM menu LIMIT 1")
    menu_id = cursor.fetchone()[0]

    assert isinstance(menu_id, int)
    print("PASS: Menu ID was generated successfully.")

finally:
    database.disconnect()
    print("PASS: Database disconnected.")
