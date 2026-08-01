from User import User

# ARRANGE / ACT
user = User(
    "testuser",
    "customer",
    "Vanisha",
    "Pierce",
    "test@example.com",
    "555-123-4567",
    "password123"
)

# ASSERT

assert user.user_name == "testuser"
assert user.account == "customer"
assert user.first_name == "Vanisha"
assert user.last_name == "Pierce"
assert user.email == "test@example.com"
assert user.phone_num == "555-123-4567"
assert user.password == "password123"

print("PASS: User object was created successfully.")
print("PASS: All seven User attributes were assigned correctly.")