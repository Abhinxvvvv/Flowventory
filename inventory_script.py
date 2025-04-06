import json

import os

INVENTORY_FILE = "inventory.json"

def load_inventory():
    """Loads medical inventory from JSON file."""
    print(f"🔍 Looking for inventory file at: {os.path.abspath(INVENTORY_FILE)}")

    if os.path.exists(INVENTORY_FILE):
        try:
            with open(INVENTORY_FILE, "r") as file:
                data = json.load(file)
                print("✅ Inventory loaded successfully!")
                return data
        except Exception as e:
            print(f"❌ Error reading inventory.json: {e}")
            return []
    else:
        print("⚠️ inventory.json not found! Creating a new one.")
        return []

def save_inventory(inventory):
    """Saves updated inventory back to JSON file."""
    with open("inventory.json", "w") as file:
        json.dump(inventory, file, indent=4)

def display_inventory(inventory):
    """Displays all medical products with quantity and price."""
    print("\n📦 Medical Inventory:")
    for item in inventory:
        print(f"🩺 {item['product_name']}: {item['quantity']} units | ₹{item['price']} each")
    print()

def restock_inventory(inventory):
    """Allows user to restock a medical product."""
    display_inventory(inventory)
    product_name = input("Enter the product name to restock: ").strip()

    for item in inventory:
        if item["product_name"].lower() == product_name.lower():
            add_qty = int(input(f"How many {product_name} to add? "))
            item["quantity"] += add_qty
            print(f"✅ {add_qty} units added to {product_name}. New stock: {item['quantity']}")
            save_inventory(inventory)
            return

    print("❌ Product not found in inventory.")

def adjust_price(inventory):
    """Allows user to adjust the price of a product."""
    display_inventory(inventory)
    product_name = input("Enter the product name to change price: ").strip()

    for item in inventory:
        if item["product_name"].lower() == product_name.lower():
            new_price = int(input(f"Enter new price for {product_name}: ₹"))
            item["price"] = new_price
            print(f"✅ Price updated! New price of {product_name}: ₹{new_price}")
            save_inventory(inventory)
            return

    print("❌ Product not found in inventory.")

def forecast_sales(inventory):
    """Predicts stock needed for next month and shows price suggestions."""
    print("\n📊 Medical Inventory Forecast (Next Month)")

    for item in inventory:
        sales_history = item.get("sales_last_3_months", [])

        if not sales_history or len(sales_history) < 3:
            print(f"⚠️ Not enough sales data for {item['product_name']}")
            continue

        avg_sales = sum(sales_history) // len(sales_history)
        predicted_demand = int(avg_sales * 1.1)  

        print(f"\n🩺 {item['product_name']}:")
        print(f"   💰 Current Price: ₹{item['price']}")
        print(f"   📉 Past 3 Months Sales: {sales_history}")
        print(f"   🔮 Predicted Demand: {predicted_demand}")
        print(f"   📦 Current Stock: {item['quantity']}")

        if item["quantity"] < predicted_demand:
            needed = predicted_demand - item["quantity"]
            print(f"   ⚠️ Restock Needed: Order {needed} more units!")

        
        if predicted_demand > avg_sales:
            suggested_price = int(item["price"] * 1.05)  # Increase by 5%
            print(f"   💰 Suggested Price: ₹{suggested_price} (Demand is high!)")
        else:
            print(f"   ✅ Price is stable at ₹{item['price']}")

    print()


def main():
    inventory = load_inventory()

    while True:
        print("\n🏥 MEDICAL INVENTORY SYSTEM")
        print("1️⃣ View Inventory")
        print("2️⃣ Restock Item")
        print("3️⃣ Adjust Price")
        print("4️⃣ Forecast Sales")
        print("5️⃣ Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            display_inventory(inventory)
        elif choice == "2":
            restock_inventory(inventory)
        elif choice == "3":
            adjust_price(inventory)
        elif choice == "4":
            forecast_sales(inventory)
        elif choice == "5":
            print("🚪 Exiting system. Goodbye!")
            break
        else:
            print("❌ Invalid choice! Please enter a number between 1-5.")

if __name__ == "__main__":
    main()
