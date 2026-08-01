from unittest.mock import patch

from DbManager import DbManager


database = DbManager()

try:
    database.connect()
    database.create_user_table("user.tsv")

    admin = database.get_admin("admin")

    print("ADMIN DATABASE BEFORE UPDATE:")
    print(admin.db)
    print("Same database object:", admin.db is database)

    with patch(
        "builtins.input",
        side_effect=[
            "9145551234",
            "updated_admin@example.com"
        ]
    ):
        result = admin.update_admin_profile(admin)

    print("\nRETURN VALUE:")
    print(repr(result))

    updated_admin = database.get_admin("admin")

    print("\nUPDATED VALUES:")
    print("Phone:", repr(updated_admin.phone_num))
    print("Email:", repr(updated_admin.email))

finally:
    database.disconnect()