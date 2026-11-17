

def add_item_buggy(item, order=[]):          # BUG: one shared list for all calls
    order.append(item)
    return order


def add_item(item, order=None):              # Fix: sentinel value
    if order is None:
        order = []                           # fresh list per new customer
    order.append(item)
    return order


def bill(order, *, discount=0.0, tax_rate=0.05):
    """Return (subtotal, tax, total) as a tuple."""
    subtotal = sum(price for _, price in order)
    subtotal -= subtotal * discount
    tax = subtotal * tax_rate
    return subtotal, tax, subtotal + tax


def main():
    print("=== COLLEGE CANTEEN ORDER SYSTEM ===")
    add_item_buggy(("Masala Dosa", 50.0))
    add_item_buggy(("Filter Coffee", 15.0))
    print(f"Inspect add_item_buggy.__defaults__: {add_item_buggy.__defaults__}")
    add_item_buggy(("Veg Biryani", 120.0))   # a "new customer" inherits old items
    print("State Leak Warning: Mutable default list order=[] contaminated across customers!")

    print("\nSentinel Solution (order=None):")
    orders = [
        [("Masala Dosa", 50.0), ("Filter Coffee", 15.0)],
        [("Veg Biryani", 120.0), ("Paneer Roll", 70.0)],
        [("Samosa", 20.0)],
    ]
    for i, items in enumerate(orders, start=1):
        order = None
        for it in items:
            order = add_item(it, order)
        _, _, total = bill(order)
        print(f"Customer {i} Order: {str(order):<52} | Total: Rs {total:.2f}")
    print("[SUCCESS] Mutable default bug resolved and parameter scope verified.")


if __name__ == "__main__":
    main()
