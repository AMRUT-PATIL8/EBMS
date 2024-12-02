import tkinter as tk
from tkinter import messagebox, simpledialog
from tkinter.ttk import Style
import datetime
import os

# File names
CUSTOMER_FILE = "customers.txt"
BILL_FILE = "bills.txt"
RECEIPT_FILE = "receipts.txt"

# Admin credentials
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "password"

# Ensure necessary files exist
if not os.path.exists(CUSTOMER_FILE):
    open(CUSTOMER_FILE, "w").close()

if not os.path.exists(BILL_FILE):
    open(BILL_FILE, "w").close()

if not os.path.exists(RECEIPT_FILE):
    open(RECEIPT_FILE, "w").close()


class ElectricBillManagement:
    def __init__(self, root):
        self.root = root
        self.root.title("Electric Bill Management System")
        self.root.geometry("800x600")

        # Load background image
        self.bg_image = tk.PhotoImage(file="background.png")  # Replace with your image path

        # Display the main screen
        self.main_screen()

    def set_background(self):
        """Set the background image on the current screen."""
        bg_label = tk.Label(self.root, image=self.bg_image)
        bg_label.place(relwidth=1, relheight=1)
        bg_label.lower()  # Ensure background is behind other widgets

    def clear_screen(self):
        """Clear all widgets from the screen."""
        for widget in self.root.winfo_children():
            widget.destroy()

    def main_screen(self):
        """Display the main screen."""
        self.clear_screen()
        self.set_background()

        tk.Label(self.root, text="Admin Login", font=("Arial", 20, "bold"), bg="#ffffff", fg="#333").pack(pady=20)
        tk.Label(self.root, text="Username:", bg="#ffffff", fg="#333").pack(pady=5)
        self.username_entry = tk.Entry(self.root)
        self.username_entry.pack()

        tk.Label(self.root, text="Password:", bg="#ffffff", fg="#333").pack(pady=5)
        self.password_entry = tk.Entry(self.root, show="*")
        self.password_entry.pack()

        login_button = tk.Button(self.root, text="Login", font=("Arial", 12, "bold"), bg="#4CAF50", fg="white",
                                 command=self.login)
        login_button.pack(pady=20)

        self.root.bind("<Return>", lambda event: self.login())  # Bind Enter key to login

    def login(self):
        """Handle admin login."""
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            messagebox.showinfo("Login Successful", "Welcome, Admin!")
            self.dashboard()
        else:
            messagebox.showerror("Error", "Invalid username or password.")

    def dashboard(self):
        """Admin dashboard."""
        self.clear_screen()
        self.set_background()

        tk.Label(self.root, text="Admin Dashboard", font=("Arial", 20, "bold"), bg="#ffffff", fg="#333").pack(pady=20)
        tk.Button(self.root, text="Manage Bills", font=("Arial", 12, "bold"), bg="#2196F3", fg="white",
                  command=self.manage_bills).pack(pady=10)
        tk.Button(self.root, text="Register Customer", font=("Arial", 12, "bold"), bg="#FF5722", fg="white",
                  command=self.register_customer).pack(pady=10)
        tk.Button(self.root, text="Logout", font=("Arial", 12, "bold"), bg="#f44336", fg="white",
                  command=self.main_screen).pack(pady=10)

    def register_customer(self):
        """Register a new customer."""
        name = simpledialog.askstring("Customer Name", "Enter customer name:")
        if not name:
            return
        email = simpledialog.askstring("Customer Email", "Enter customer email:")
        if not email:
            return
        address = simpledialog.askstring("Customer Address", "Enter customer address:")
        if not address:
            return
        connection_id = simpledialog.askstring("Connection ID", "Enter a unique connection ID:")
        if not connection_id:
            return

        with open(CUSTOMER_FILE, "a") as f:
            f.write(f"{connection_id},{name},{email},{address}\n")
        messagebox.showinfo("Success", "Customer registered successfully!")

    def find_customer(self, connection_id):
        """Find a customer by connection ID."""
        with open(CUSTOMER_FILE, "r") as f:
            for line in f:
                if line.startswith(connection_id + ","):
                    return line.strip().split(",")
        return None

    def manage_bills(self):
        """Manage customer bills."""
        connection_id = simpledialog.askstring("Connection ID", "Enter customer connection ID:")
        if not connection_id:
            return
        customer = self.find_customer(connection_id)
        if customer:
            self.bill_screen(customer)
        else:
            if messagebox.askyesno("Not Found", "Customer not found. Would you like to register?"):
                self.register_customer()

    def bill_screen(self, customer):
        """Bill calculation screen."""
        self.clear_screen()
        self.set_background()

        tk.Label(self.root, text=f"Customer: {customer[1]}", font=("Arial", 16, "bold"), bg="#ffffff", fg="#333").pack(pady=10)
        tk.Label(self.root, text=f"Email: {customer[2]}", bg="#ffffff", fg="#333").pack()
        tk.Label(self.root, text=f"Address: {customer[3]}", bg="#ffffff", fg="#333").pack()

        tk.Label(self.root, text="Units Consumed:", bg="#ffffff", fg="#333").pack(pady=5)
        self.units_entry = tk.Entry(self.root)
        self.units_entry.pack()

        tk.Button(self.root, text="Calculate Bill", font=("Arial", 12, "bold"), bg="#4CAF50", fg="white",
                  command=lambda: self.calculate_bill(customer)).pack(pady=10)
        tk.Button(self.root, text="Back", font=("Arial", 12, "bold"), bg="#f44336", fg="white",
                  command=self.dashboard).pack(pady=10)

    def calculate_bill(self, customer):
        """Calculate the bill and record it."""
        try:
            units = int(self.units_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number of units.")
            return

        if units <= 100:
            rate = 3.0
        elif units <= 300:
            rate = 4.5
        else:
            rate = 6.0
        total = round(units * rate, 2)

        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(BILL_FILE, "a") as f:
            f.write(f"{customer[0]},{units},{total},{timestamp}\n")

        self.payment_screen(customer, units, total)

    def payment_screen(self, customer, units, total):
        """Display payment options and generate receipt."""
        self.clear_screen()
        self.set_background()

        tk.Label(self.root, text=f"Total Bill: ₹{total}", font=("Arial", 16, "bold"), bg="#ffffff", fg="#333").pack(pady=20)
        tk.Label(self.root, text="Choose Payment Method:", bg="#ffffff", fg="#333").pack(pady=10)

        tk.Button(self.root, text="Credit Card", font=("Arial", 12, "bold"), bg="#2196F3", fg="white",
                  command=lambda: self.generate_receipt(customer, units, total, "Credit Card")).pack(pady=5)
        tk.Button(self.root, text="UPI", font=("Arial", 12, "bold"), bg="#4CAF50", fg="white",
                  command=lambda: self.generate_receipt(customer, units, total, "UPI")).pack(pady=5)
        tk.Button(self.root, text="Cash", font=("Arial", 12, "bold"), bg="#FF5722", fg="white",
                  command=lambda: self.generate_receipt(customer, units, total, "Cash")).pack(pady=5)

    def generate_receipt(self, customer, units, total, payment_method):
        """Generate and save the payment receipt."""
        receipt_text = f"""
        ===== Payment Receipt =====
        Connection ID: {customer[0]}
        Name: {customer[1]}
        Units Consumed: {units}
        Total Bill: ₹{total}
        Payment Method: {payment_method}
        Date & Time: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        ============================
        """

        with open(RECEIPT_FILE, "a", encoding="utf-8") as f:
            f.write(receipt_text + "\n")

        messagebox.showinfo("Payment Successful", "Receipt generated successfully!")
        self.dashboard()


if __name__ == "__main__":
    root = tk.Tk()
    app = ElectricBillManagement(root)
    root.mainloop()
