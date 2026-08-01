from DbManager import DbManager
from Users import Admin

# ARRANGE
database = DbManager()
database.connect()
database.create_menu_table("menu.tsv")

admin = Admin(
    "testadmin",
    "admin",
    "Test",
    "Admin",
    "test@email.com",
    "1234567890",
    "password",
    "FV9999"
)

# ACT
admin.manage_menu(database)

# CHECK DATABASE
cursor = database.conn.cursor()

cursor.execute("""
    SELECT item_name,
            description,
            price,
            available
    FROM menu
    WHERE item_name = ?
""", ("Cheeseburger",))

result = cursor.fetchone()

print()
print("DATABASE RESULT:")
print(result)

database.disconnect()