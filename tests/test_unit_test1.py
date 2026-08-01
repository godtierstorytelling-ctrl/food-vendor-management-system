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

print("\nUPDATED OBJECT:")
print("Phone:", repr(admin.phone_num))
print("Email:", repr(admin.email))