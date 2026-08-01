from FoodVendor import FoodVendor


vendor = FoodVendor()

choice = vendor.main_menu()

print()
print("RETURNED CHOICE:")
print(choice)
print(type(choice))