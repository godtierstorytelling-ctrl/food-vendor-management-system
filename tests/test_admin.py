from Users import User, Admin

# ARRANGE / ACT
admin = Admin(
    "testuser",
    "admin",
    "Vanisha",
    "Pierce",
    "test@example.com",
    "555-123-4567",
    "password123",
    "EMP001"
)

# ASSERT
assert admin.user_name == "testuser"
assert admin.account == "admin"
assert admin.first_name == "Vanisha"
assert admin.last_name == "Pierce"
assert admin.email == "test@example.com"
assert admin.phone_num == "555-123-4567"
assert admin.password == "password123"

# Test Admin-specific attribute
assert admin.employ_id == "EMP001"

# ASSERT STRING REPRESENTATION
expected_output = "Vanisha Pierce: testuser, Employee ID: EMP001"

actual_output = str(admin)

assert actual_output == expected_output

# Test inheritance itself
assert isinstance(admin, Admin)
assert isinstance(admin, User)

print("PASS: Admin object was created successfully.")
print("PASS: All seven inherited User attributes were assigned correctly.")
print("PASS: Admin-specific employ_id is correct.")
print("PASS: Admin __str__() output matches exactly.")
print(f"Output: {actual_output}")
