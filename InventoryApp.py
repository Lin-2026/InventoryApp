import os
import json
import tkinter as tk
from tkinter import messagebox, simpledialog

# File names
SIGN_UP_FILE = "sign_up_info.JSON"
INVENTORY_FILE = "inventory.JSON"

# Initialize files if they do not exist
def initialize_files():
    if not os.path.exists(SIGN_UP_FILE):
        with open(SIGN_UP_FILE, 'w') as file:
            # Initialize with a preset admin account
            file.write(json.dumps({"admin": "admin123"}))
    if not os.path.exists(INVENTORY_FILE):
        with open(INVENTORY_FILE, 'w') as file:
            file.write(json.dumps([]))

def read_file(file_name):
    with open(file_name, 'r') as file:
        return json.loads(file.read())

def write_file(file_name, data):
    with open(file_name, 'w') as file:
        file.write(json.dumps(data, indent=4))

# GUI Functions
def sign_up_gui():
    def create_account():
        username = username_entry.get()
        password = password_entry.get()
        users = read_file(SIGN_UP_FILE)
        if username in users:
            messagebox.showerror("Error", "Username already exists!")
        else:
            users[username] = password
            write_file(SIGN_UP_FILE, users)
            messagebox.showinfo("Success", "Account created successfully!")
            signup_window.destroy()

    def back():
        signup_window.destroy()

    signup_window = tk.Toplevel()
    signup_window.title("Sign Up")
    signup_window.geometry("400x300")
    signup_window.configure(bg="#f0f8ff")

    tk.Label(signup_window, text="Create an Account", font=("Arial", 16), bg="#f0f8ff").pack(pady=10)
    tk.Label(signup_window, text="Username:", bg="#f0f8ff").pack(pady=5)
    username_entry = tk.Entry(signup_window)
    username_entry.pack(pady=5)

    tk.Label(signup_window, text="Password:", bg="#f0f8ff").pack(pady=5)
    password_entry = tk.Entry(signup_window, show="*")
    password_entry.pack(pady=5)

    tk.Button(signup_window, text="Create Account", command=create_account).pack(pady=10)
    tk.Button(signup_window, text="Back", command=back).pack(pady=5)

def login_gui():
    def authenticate():
        username = username_entry.get()
        password = password_entry.get()
        users = read_file(SIGN_UP_FILE)
        if username in users and users[username] == password:
            login_window.destroy()
            if username == "admin":
                admin_menu()
            else:
                messagebox.showinfo("Success", "Login successful!")
                user_menu(username)
        else:
            messagebox.showerror("Error", "Invalid username or password.")

    def back():
        login_window.destroy()

    login_window = tk.Toplevel()
    login_window.title("Login")
    login_window.geometry("400x300")
    login_window.configure(bg="#f0f8ff")

    tk.Label(login_window, text="Welcome Back!", font=("Arial", 16), bg="#f0f8ff").pack(pady=10)
    tk.Label(login_window, text="Username:", bg="#f0f8ff").pack(pady=5)
    username_entry = tk.Entry(login_window)
    username_entry.pack(pady=5)

    tk.Label(login_window, text="Password:", bg="#f0f8ff").pack(pady=5)
    password_entry = tk.Entry(login_window, show="*")
    password_entry.pack(pady=5)

    tk.Button(login_window, text="Login", command=authenticate).pack(pady=10)
    tk.Button(login_window, text="Back", command=back).pack(pady=5)

def admin_menu():
    def add_item():
        barcode = simpledialog.askstring("Add Item", "Enter barcode:")
        name = simpledialog.askstring("Add Item", "Enter name:")
        description = simpledialog.askstring("Add Item", "Enter description:")
        price = simpledialog.askfloat("Add Item", "Enter price:")
        quantity = simpledialog.askinteger("Add Item", "Enter quantity:")

        inventory = read_file(INVENTORY_FILE)
        inventory.insert(0, {"barcode": barcode, "name": name, "description": description, "price": price, "quantity": quantity})
        write_file(INVENTORY_FILE, inventory)
        messagebox.showinfo("Success", "Item added successfully!")

    def remove_item():
        barcode = simpledialog.askstring("Remove Item", "Enter barcode of the item to remove:")
        inventory = read_file(INVENTORY_FILE)
        inventory = [item for item in inventory if item["barcode"] != barcode]
        write_file(INVENTORY_FILE, inventory)
        messagebox.showinfo("Success", "Item removed successfully!")

    def update_quantity():
        barcode = simpledialog.askstring("Update Quantity", "Enter barcode of the item:")
        new_quantity = simpledialog.askinteger("Update Quantity", "Enter the new quantity:")

        inventory = read_file(INVENTORY_FILE)
        for item in inventory:
            if item["barcode"] == barcode:
                item["quantity"] = new_quantity
                break
        else:
            messagebox.showerror("Error", "Item not found.")
            return

        write_file(INVENTORY_FILE, inventory)
        messagebox.showinfo("Success", "Quantity updated successfully!")

    admin_window = tk.Toplevel()
    admin_window.title("Admin Menu")
    admin_window.geometry("500x400")
    admin_window.configure(bg="#e6f7ff")

    tk.Label(admin_window, text="Admin Panel", font=("Arial", 18), bg="#e6f7ff").pack(pady=10)
    tk.Button(admin_window, text="Add Item", command=add_item).pack(pady=10)
    tk.Button(admin_window, text="Remove Item", command=remove_item).pack(pady=10)
    tk.Button(admin_window, text="Update Quantity", command=update_quantity).pack(pady=10)
    tk.Button(admin_window, text="Logout", command=admin_window.destroy).pack(pady=10)

def user_menu(username):
    inventory = read_file(INVENTORY_FILE)
    shopping_list_file = f"{username}_shopping_list.JSON"
    if not os.path.exists(shopping_list_file):
        write_file(shopping_list_file, [])
    shopping_list = read_file(shopping_list_file)

    def add_to_cart():
        barcode = simpledialog.askstring("Add to Cart", "Enter the barcode of the item to add:")
        item = next((item for item in inventory if item["barcode"] == barcode), None)
        if item:
            if item["quantity"] > 0:
                item["quantity"] -= 1
                if item["quantity"] == 0:
                    inventory.remove(item)  # Remove the item if quantity becomes zero
                shopping_list.append({"name": item["name"], "price": item["price"], "description": item["description"], "barcode": item["barcode"]})
                write_file(INVENTORY_FILE, inventory)
                write_file(shopping_list_file, shopping_list)
                refresh_display()
                messagebox.showinfo("Success", "Item added to shopping list!")
            else:
                messagebox.showerror("Error", "Item is out of stock.")
        else:
            messagebox.showerror("Error", "Item not found.")

    def refresh_display():
        inventory_list.delete(0, tk.END)
        for item in inventory:
            inventory_list.insert(tk.END, f"Barcode ID: {item['barcode']} - Name: {item['name']} - ${item['price']}\nDescription: {item['description']} - Quantity: {item['quantity']}")
        shopping_list_display.delete(0, tk.END)
        for item in shopping_list:
            shopping_list_display.insert(tk.END, f"Barcode ID: {item['barcode']} - Name: {item['name']} - ${item['price']}\nDescription: {item['description']}")

    user_window = tk.Toplevel()
    user_window.title("User Menu")
    user_window.geometry("600x600")
    user_window.configure(bg="#f0fff0")

    tk.Label(user_window, text="Inventory:", font=("Arial", 14), bg="#f0fff0").pack(pady=5)
    inventory_list = tk.Listbox(user_window, width=60)
    inventory_list.pack(pady=5)

    tk.Label(user_window, text="Your Shopping List:", font=("Arial", 14), bg="#f0fff0").pack(pady=5)
    shopping_list_display = tk.Listbox(user_window, width=60)
    shopping_list_display.pack(pady=5)

    tk.Button(user_window, text="Add to Shopping List", command=add_to_cart).pack(pady=10)
    tk.Button(user_window, text="Logout", command=user_window.destroy).pack(pady=10)

    refresh_display()

def main():
    initialize_files()

    root = tk.Tk()
    root.title("Inventory App")
    root.geometry("400x300")
    root.configure(bg="#faf0e6")

    tk.Label(root, text="Welcome to Inventory App", font=("Arial", 18), bg="#faf0e6").pack(pady=20)
    tk.Button(root, text="Sign Up", command=sign_up_gui).pack(pady=10)
    tk.Button(root, text="Login", command=login_gui).pack(pady=10)
    tk.Button(root, text="Exit", command=root.quit).pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()
