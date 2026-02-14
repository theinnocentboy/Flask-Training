# Scenario 01
# You are developing a user registration module for a web application.
# Store user details such as username, age, email and is active using appropriate data types and display them.

username = input("Enter username:")
age = int(input("Enter Age:"))
email = input("Enter email address:")
is_active = True

print(f"User:{username}\nAge:{age}\nEmail:{email}\nIs Active:{is_active}")

# Scenario 02
# A startup is building a priceing calculator API.
# Store product price, discount percentage, and final price using correct data types and print rhe result.
prodPrice = float(input("Enter price: "))
discountRate = float(input("Enter discount (in percentage): "))
finalPrice = prodPrice * (1 - discountRate/100)

print(f"MRP: {prodPrice} and Sale Price: {finalPrice}")