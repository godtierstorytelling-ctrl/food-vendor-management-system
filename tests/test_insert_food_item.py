from DbManager import DbManager
from Users import Admin

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

admin.insert_food_item(database)

cursor = database.conn.cursor()

cursor.execute("""
    SELECT category,
           item_name,
           description,
           price,
           prep_time,
           available
    FROM menu
    WHERE item_name = ?
""", ("Salsa Roja",))

result = cursor.fetchone()

print()
print("DATABASE RESULT:")
print(result)

database.disconnect()