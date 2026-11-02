from collections import deque
from datetime import datetime, timedelta
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

# =====================================================
# SMART CAMPUS FOOD PRE-ORDER SYSTEM (CLI VERSION)
# =====================================================

# Food Menu
menu = {
    1: ("Burger", 60),
    2: ("Pizza", 100),
    3: ("Sandwich", 50),
    4: ("Samosa", 20),
    5: ("Chole Bhature", 80),
    6: ("Cold Drink", 40),
    7: ("Coffee", 30),
    8: ("Tea", 20)
}

# Queue
order_queue = deque()

# Order number
order_number = 1000

# =====================================================
# DISPLAY MENU
# =====================================================

def show_menu():
    print("\n" + "=" * 50)
    print("              CAMPUS FOOD MENU")
    print("=" * 50)
    for number, item in menu.items():
        print(f"{number}. {item[0]:<20} ₹{item[1]}")
    print("=" * 50)

# =====================================================
# PLACE ORDER
# =====================================================

def place_order():
    global order_number
    print("\n========== PLACE PRE-ORDER ==========")
    name = input("Enter student name: ").strip()
    roll_no = input("Enter roll number: ").strip()

    cart = []

    while True:
        show_menu()
        try:
            choice = int(input("Select food (0 = Finish): "))
        except ValueError:
            print("Please enter a valid number.")
            continue

        if choice == 0:
            break

        if choice not in menu:
            print("Invalid food item.")
            continue

        try:
            quantity = int(input("Enter quantity: "))
        except ValueError:
            print("Enter a valid quantity.")
            continue

        if quantity <= 0:
            print("Quantity must be greater than zero.")
            continue

        food_name, price = menu[choice]
        cart.append({
            "name": food_name,
            "price": price,
            "quantity": quantity
        })
        print(f"✓ {food_name} added to your order.")

    if not cart:
        print("\nNo items selected.")
        return

    # Calculate bill
    subtotal = sum(item["price"] * item["quantity"] for item in cart)

    # 10% Discount if subtotal >= 300
    discount = subtotal * 0.10 if subtotal >= 300 else 0
    total = subtotal - discount

    # Generate token
    order_number += 1
    token = order_number

    # Queue position
    position = len(order_queue) + 1
    waiting_time = position * 5
    pickup_time = (datetime.now() + timedelta(minutes=waiting_time)).strftime("%I:%M %p")

    # Create order
    order = {
        "token": token,
        "name": name,
        "roll_no": roll_no,
        "items": cart,
        "subtotal": subtotal,
        "discount": discount,
        "total": total,
        "status": "Preparing",
        "position": position,
        "pickup": pickup_time
    }

    order_queue.append(order)

    # Print receipt
    print("\n")
    print("=" * 50)
    print("              ORDER CONFIRMED")
    print("=" * 50)
    print(f"Token Number : {token}")
    print(f"Student      : {name}")
    print(f"Roll Number  : {roll_no}")
    print("\nOrdered Items")
    print("-" * 50)
    for item in cart:
        amount = item["price"] * item["quantity"]
        print(f"{item['name']:<20} x {item['quantity']:<3} ₹{amount}")
    print("-" * 50)
    print(f"Subtotal     : ₹{subtotal:.2f}")
    print(f"Discount     : ₹{discount:.2f}")
    print(f"Total        : ₹{total:.2f}")
    print("-" * 50)
    print(f"Queue Position  : {position}")
    print(f"Estimated Pickup: {pickup_time}")
    print("=" * 50)
    print("\n✓ Please show your token at the campus canteen.")

# =====================================================
# CHECK ORDER
# =====================================================

def check_order():
    print("\n========== CHECK ORDER ==========")
    try:
        token = int(input("Enter your token number: "))
    except ValueError:
        print("Invalid token.")
        return

    for position, order in enumerate(order_queue, start=1):
        if order["token"] == token:
            people_ahead = position - 1
            print("\n" + "=" * 45)
            print("             ORDER STATUS")
            print("=" * 45)
            print(f"Token Number : {order['token']}")
            print(f"Student      : {order['name']}")
            print(f"Roll Number  : {order['roll_no']}")
            print(f"Status       : {order['status']}")
            print(f"Queue Position: {position}")
            print(f"People Ahead : {people_ahead}")
            print(f"Pickup Time  : {order['pickup']}")
            print(f"Total Bill   : ₹{order['total']:.2f}")
            print("=" * 45)
            return

    print("\n❌ Order not found.")

# =====================================================
# CANCEL ORDER
# =====================================================

def cancel_order():
    print("\n========== CANCEL ORDER ==========")
    try:
        token = int(input("Enter token number: "))
    except ValueError:
        print("Invalid token.")
        return

    for order in order_queue:
        if order["token"] == token:
            order_queue.remove(order)
            print(f"\n✓ Order {token} cancelled successfully.")
            return

    print("\n❌ Order not found.")

# =====================================================
# MAIN MENU
# =====================================================

def main():
    while True:
        print("\n")
        print("=" * 55)
        print("       SMART CAMPUS FOOD PRE-ORDER")
        print("=" * 55)
        print("1. Place Food Pre-Order")
        print("2. Check Order Status")
        print("3. Cancel Order")
        print("4. Exit")
        print("=" * 55)

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            place_order()
        elif choice == "2":
            check_order()
        elif choice == "3":
            cancel_order()
        elif choice == "4":
            print("\nThank you for using Smart Campus Food Pre-Order System!")
            break
        else:
            print("\n❌ Invalid choice. Please select 1-4.")

if __name__ == "__main__":
    main()
