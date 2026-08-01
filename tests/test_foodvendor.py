from DbManager import DbManager
from FoodVendor import FoodVendor

database = DbManager()
food_vendor = FoodVendor()

try:
    # Test initialization
    food_vendor.initialize(database)

    # Confirm FoodVendor stored the supplied DbManager
    assert food_vendor.db is database
    print("PASS: FoodVendor stored the DbManager object.")

    # Confirm database connection exists
    assert food_vendor.db.conn is not None
    print("PASS: Database connection established.")

    cursor = food_vendor.db.conn.cursor()

    # Confirm menu table exists
    cursor.execute("""
        SELECT name
        FROM sqlite_master
        WHERE type = 'table' AND name = 'menu'
    """)
    
    assert cursor.fetchone() is not None
    print("PASS: Menu table exists.")
    
    # Confirm menu records loaded
    cursor.execute("SELECT COUNT(*) FROM menu")
    menu_count = cursor.fetchone()[0]

    assert menu_count > 0
    print(f"PASS: Menu table contains {menu_count} records.")

    # Confirm user table exists
    cursor.execute("""
        SELECT name
        FROM sqlite_master
        WHERE type = 'table' AND name = 'user'
        """)
    
    assert cursor.fetchone() is not None
    print("PASS: User table exists.")

    # Confirm user records loaded
    cursor.execute("SELECT COUNT(*) FROM user")
    user_count = cursor.fetchone()[0]

    assert user_count > 0
    print(f"PASS: User table contains {user_count} records.")

    print("\nPHASE 3 PASSED!")

finally:
    database.disconnect()
    print("PASS: Database disconnected.")