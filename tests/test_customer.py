from Users import User, Customer

# TEST 1: Guest customer
guest = Customer()

assert guest.user_name == "Guest"
assert guest.account == ""
assert guest.first_name == ""
assert guest.last_name == ""
assert guest.email == ""
assert guest.phone_num == ""
assert guest.password == ""
assert guest.card_num == ""
assert guest.card_date == ""
assert guest.address == ""
assert guest.points == 0
assert guest.history == 0

print("PASS: Guest Customer object created successfully.")
print("PASS: All default Customer values are correct.")

# TEST 2: Fully populated customer
customer = Customer(
    "testcustomer",
    "customer",
    "Vanisha",
    "Pierce",
    "test@example.com",
    "555-123-4567",
    "password123",
    "4111111111111111",
    "12/28",
    "123 Test Street",
    100,
    42
)

assert customer.user_name == "testcustomer"
assert customer.account == "customer"
assert customer.first_name == "Vanisha"
assert customer.last_name == "Pierce"
assert customer.email == "test@example.com"
assert customer.phone_num == "555-123-4567"
assert customer.password == "password123"

assert customer.card_num == "4111111111111111"
assert customer.card_date == "12/28"
assert customer.address == "123 Test Street"
assert customer.points == 100
assert customer.history == 42

assert isinstance(customer, Customer)
assert isinstance(customer, User)

print("PASS: Fully populated Customer object created successfully.")
print("PASS: All inherited User attributes are correct.")
print("PASS: All Customer-specific attributes are correct.")
print("PASS: Customer is also recognized as a User.")

expected_output = "Vanisha Pierce: testcustomer, Rewards: 100"

actual_output = str(customer)

assert actual_output == expected_output

print("PASS: Customer __str__() output matches exactly.")
print(f"Output: {actual_output}")

assert guest.user_name == "Guest"
assert isinstance(guest.points, int)
assert isinstance(guest.history, int)

print("PASS: Guest username defaults to 'Guest'.")
print("PASS: Customer numeric defaults are integers.")