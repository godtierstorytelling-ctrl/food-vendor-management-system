from unittest.mock import patch

from Users import Admin


admin = Admin(
    "admin",
    "admin",
    "afirst",
    "alast",
    "admin@example.com",
    "1234567890",
    "password",
    "FV1001"
)

print("DATABASE BEFORE UPDATE:")
print(admin.db)

try:
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

    print("\nDATABASE AFTER UPDATE:")
    print(admin.db)

except Exception as error:
    print("\nERROR TYPE:")
    print(type(error).__name__)

    print("\nERROR MESSAGE:")
    print(str(error))