import tkinter as tk
from tkinter import messagebox
import json
import os

INVENTORY_FILE = os.path.join(os.path.dirname(__file__), "inventory.json")

def load_inventory():
    try:
        with open(INVENTORY_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def save_inventory():
    with open(INVENTORY_FILE, "w") as file:
        json.dump(inventory, file, indent=4)

def display_inventory():
    text_area.delete("1.0", tk.END)
    text_area.insert(tk.END, "📦 Medical Inventory:\n\n")
    for item in inventory:
        text_area.insert(tk.END, f"🩺 {item['product_name']} - {item['quantity']} units - ₹{item['price']}\n")

def restock_item():
    name = entry_name.get().strip()
    qty = entry_qty.get().strip()
    if not name or not qty.isdigit():
        messagebox.showerror("Input Error", "Enter valid product name and quantity")
        return

    for item in inventory:
        if item["product_name"].lower() == name.lower():
            item["quantity"] += int(qty)
            save_inventory()
            display_inventory()
            messagebox.showinfo("Success", f"Restocked {qty} units of {name}.")
            reset_placeholders()
            return
    messagebox.showerror("Error", "Product not found.")

def adjust_price():
    name = entry_name.get().strip()
    price = entry_price.get().strip()
    if not name or not price.isdigit():
        messagebox.showerror("Input Error", "Enter valid product name and price")
        return

    for item in inventory:
        if item["product_name"].lower() == name.lower():
            item["price"] = int(price)
            save_inventory()
            display_inventory()
            messagebox.showinfo("Success", f"Updated price of {name} to ₹{price}.")
            reset_placeholders()
            return
    messagebox.showerror("Error", "Product not found.")

def forecast_sales():
    text_area.delete("1.0", tk.END)
    text_area.insert(tk.END, "📊 Sales Forecast:\n\n")

    for item in inventory:
        sales_history = item.get("sales_last_3_months", [])
        if len(sales_history) < 3:
            text_area.insert(tk.END, f"⚠️ Not enough sales data for {item['product_name']}\n")
            continue

        avg_sales = sum(sales_history) // len(sales_history)
        predicted_demand = int(avg_sales * 1.1)
        suggested_price = int(item["price"] * 1.05)

        text_area.insert(tk.END, f"🩺 {item['product_name']}\n")
        text_area.insert(tk.END, f"   🔮 Predicted Demand: {predicted_demand} units\n")
        text_area.insert(tk.END, f"   💰 Current Price: ₹{item['price']} | Suggested Price: ₹{suggested_price}\n\n")

def clear_placeholder(event, entry, placeholder):
    if entry.get() == placeholder:
        entry.delete(0, tk.END)

def restore_placeholder(event, entry, placeholder):
    if not entry.get():
        entry.insert(0, placeholder)

def setup_entry(root, placeholder):
    entry = tk.Entry(root, width=30)
    entry.insert(0, placeholder)
    entry.bind("<FocusIn>", lambda event: clear_placeholder(event, entry, placeholder))
    entry.bind("<FocusOut>", lambda event: restore_placeholder(event, entry, placeholder))
    entry.pack(pady=5)
    return entry

def reset_placeholders():
    entry_name.delete(0, tk.END)
    entry_name.insert(0, "Enter Product Name")

    entry_qty.delete(0, tk.END)
    entry_qty.insert(0, "Enter Quantity")

    entry_price.delete(0, tk.END)
    entry_price.insert(0, "Enter New Price")

root = tk.Tk()
root.title("Medical Inventory System")
root.geometry("500x500")

inventory = load_inventory()

entry_name = setup_entry(root, "Enter Product Name")
entry_qty = setup_entry(root, "Enter Quantity")
entry_price = setup_entry(root, "Enter New Price")

tk.Button(root, text="View Inventory", command=display_inventory).pack(pady=5)
tk.Button(root, text="Restock Item", command=restock_item).pack(pady=5)
tk.Button(root, text="Adjust Price", command=adjust_price).pack(pady=5)
tk.Button(root, text="Forecast Sales", command=forecast_sales).pack(pady=5)

text_area = tk.Text(root, height=10, width=50)
text_area.pack(pady=10)

display_inventory()

root.mainloop()
