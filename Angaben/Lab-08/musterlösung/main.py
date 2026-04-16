from decorators import deposit, get_balance

print("--- Test 1: deposit ---")
result = deposit("AT12345", 500)
print(f"Return value: {result}")
print(f"Function name: {deposit.__name__}") # Korrekt: 'deposit'
print(f"Function docstring: {deposit.__doc__}") # Korrekt: Zeigt Docstring

print("\n--- Test 2: get_balance ---")
balance = get_balance("AT98765")
print(f"Return value: {balance}")
print(f"Function name: {get_balance.__name__}") # Korrekt: 'get_balance'