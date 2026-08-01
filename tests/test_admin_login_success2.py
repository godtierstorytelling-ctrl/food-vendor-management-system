from DbManager import DbManager


database = DbManager()

try:
    database.connect()
    database.create_user_table("user.tsv")

    admin = database.get_admin("admin")

    print("Username:", repr(admin.user_name))
    print("Account:", repr(admin.account))
    print("Password:", repr(admin.password))
    print("Employee ID:", repr(admin.employ_id))

finally:
    database.disconnect()