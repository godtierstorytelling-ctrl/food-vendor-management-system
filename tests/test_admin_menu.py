from DbManager import DbManager
from Users import Admin


# ARRANGE
database = DbManager()
database.connect()
database.create_menu_table("menu.tsv")
database.create_user_table("user.tsv")

admin = Admin(
    "testadmin",
    "admin",
    "Test",
    "Admin",
    "testadmin@email.com",
    "1234567890",
    "password",
    "FV9999"
)


# ACT
admin.admin_menu(database)


print()
print("ADMIN MENU FINISHED")

database.disconnect()