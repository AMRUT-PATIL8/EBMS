import tkinter as tk
from tkinter import messagebox, simpledialog
import datetime
import os
from PIL import Image, ImageTk

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
        try:
            self.bg_img = Image.open("background.png")
            self.bg_img = ImageTk.PhotoImage(self.bg_img.resize((800, 600)))
        except Exception:
            self.bg_img = None

        self.main_screen()
    
    def set_background(self):
        """Set background image for the current screen."""
        if self.bg_img:
            bg_label = tk.Label(self.root, image=self.bg_img)
            bg_label.place(relwidth=1, relheight=1)
        else:
            bg_label = tk.Label(self.root, bg="#f0f8ff")
            bg_label.place(relwidth=1, relheight=1)

    def clear_screen(self):
        """Clear the screen."""
        for widget in self.root.winfo_children():
            widget.destroy()

    def main_screen(self):
        """Display the main screen with animations."""
        self.clear_screen()
        self.set_background()

        # Initial label
        tk.Label(self.root, text="Admin Login", font=("Arial", 25, "bold"), bg="#f0f8ff").pack(pady=20)

        # Create and hide the widgets initially
        self.username_label = tk.Label(self.root, text="Username:", font=("Arial", 12), bg="#f0f8ff")
        self.username_entry = tk.Entry(self.root, font=("Arial", 12))
        self.password_label = tk.Label(self.root, text="Password:", font=("Arial", 12), bg="#f0f8ff")
        self.password_entry = tk.Entry(self.root, show="*", font=("Arial", 12))
        self.login_button = tk.Button(self.root, text="Login", font=("Arial", 12, "bold"),
                                      bg="#4caf50", fg="white", command=self.login)

        # Pack widgets with a delay for animation
        self.root.after(500, self.show_username)
        self.root.after(1000, self.show_password)
        self.root.after(1500, self.show_login_button)

        # Bind Enter key
        self.root.bind("<Return>", lambda event: self.login())
        
    def show_username(self):
        """Show the username label and entry."""
        self.username_label.pack(pady=5)
        self.username_entry.pack()

    def show_password(self):
        """Show the password label and entry."""
        self.password_label.pack(pady=5)
        self.password_entry.pack()

    def show_login_button(self):
        """Show the login button."""
        self.login_button.pack(pady=20)

    def login(self, event=None):
        """Handle admin login."""
        try:
            username = self.username_entry.get()
            password = self.password_entry.get()
        except tk.TclError:
            messagebox.showerror("Error", "Login fields are unavailable.")
            return

        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            messagebox.showinfo("Login Successful", "Welcome, Admin!")
            self.dashboard()
        else:
            messagebox.showerror("Error", "Invalid username or password.")
   

    def dashboard(self):
        """Admin dashboard."""
        self.clear_screen()
        self.set_background()

        self.root.bind("<Return>", lambda event: None)  # Unbind Enter key

        tk.Label(self.root, text="Admin Dashboard", font=("Arial", 25, "bold"), bg="#f0f8ff").pack(pady=20)
        tk.Button(self.root, text="Manage Bills", font=("Arial", 12, "bold"), bg="#4caf50", fg="white", command=self.manage_bills).pack(pady=10)
        tk.Button(self.root, text="Register Customer", font=("Arial", 12, "bold"), bg="#2196f3", fg="white", command=self.register_customer).pack(pady=10)
        tk.Button(self.root, text="Logout", font=("Arial", 12, "bold"), bg="#f44336", fg="white", command=self.main_screen).pack(pady=10)

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

        tk.Label(self.root, text=f"Customer: {customer[1]}", font=("Arial", 16, "bold"), bg="#f0f8ff").pack(pady=10)
        tk.Label(self.root, text=f"Email: {customer[2]}", bg="#f0f8ff").pack()
        tk.Label(self.root, text=f"Address: {customer[3]}", bg="#f0f8ff").pack()

        tk.Label(self.root, text="Units Consumed:", bg="#f0f8ff").pack(pady=5)
        self.units_entry = tk.Entry(self.root)
        self.units_entry.pack()

        tk.Button(self.root, text="Calculate Bill", font=("Arial", 12, "bold"), bg="#4caf50", fg="white",
                  command=lambda: self.calculate_bill(customer)).pack(pady=10)
        tk.Button(self.root, text="View Previous Bills", font=("Arial", 12, "bold"), bg="#2196f3", fg="white",
                  command=lambda: self.view_previous_bills(customer)).pack(pady=10)
        tk.Button(self.root, text="Back", font=("Arial", 12, "bold"), bg="#9e9e9e", fg="white", command=self.dashboard).pack(pady=10)

    def calculate_bill(self, customer):
        """Calculate the bill and record it."""
        try:
            units = int(self.units_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number of units.")
            return

        # Calculate bill based on units
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

        tk.Label(self.root, text=f"Total Bill: ₹{total}", font=("Arial", 16, "bold"), bg="#f0f8ff").pack(pady=20)
        tk.Label(self.root, text="Choose Payment Method:", bg="#f0f8ff").pack(pady=10)

        tk.Button(self.root, text="Credit Card", font=("Arial", 12, "bold"), bg="#4caf50", fg="white",
                  command=lambda: self.generate_receipt(customer, units, total, "Credit Card")).pack(pady=5)
        tk.Button(self.root, text="UPI", font=("Arial", 12, "bold"), bg="#2196f3", fg="white",
                  command=lambda: self.generate_receipt(customer, units, total, "UPI")).pack(pady=5)
        tk.Button(self.root, text="Cash", font=("Arial", 12, "bold"), bg="#f44336", fg="white",
                  command=lambda: self.generate_receipt(customer, units, total, "Cash")).pack(pady=5)

    def generate_receipt(self, customer, units, total, payment_method):
        """Generate and save the payment receipt."""
        receipt_content = (
            f"Customer Name: {customer[1]}\n"
            f"Connection ID: {customer[0]}\n"
            f"Units Consumed: {units}\n"
            f"Total Amount Paid: ₹{total}\n"
            f"Payment Method: {payment_method}\n"
            f"Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        )

        # Open the file with utf-8 encoding
        with open(RECEIPT_FILE, "a", encoding="utf-8") as f:
            f.write(receipt_content + "\n---\n")

        messagebox.showinfo("Payment Successful", f"Receipt:\n\n{receipt_content}")
        self.dashboard()


    def view_previous_bills(self, customer):
        """Display previous bills of a customer."""
        self.clear_screen()
        self.set_background()

        tk.Label(self.root, text=f"Previous Bills of {customer[1]}", font=("Arial", 16, "bold"), bg="#f0f8ff").pack(pady=10)
        has_bills = False

        with open(BILL_FILE, "r") as f:
            for line in f:
                data = line.strip().split(",")
                if data[0] == customer[0]:
                    has_bills = True
                    tk.Label(self.root, text=f"Date: {data[3]} | Units: {data[1]} | Amount: ₹{data[2]}",
                             font=("Arial", 12), bg="#f0f8ff").pack(pady=5)

        if not has_bills:
            tk.Label(self.root, text="No previous bills found.", bg="#f0f8ff").pack(pady=10)

        tk.Button(self.root, text="Back", font=("Arial", 12, "bold"), bg="#9e9e9e", fg="white", command=lambda: self.bill_screen(customer)).pack(pady=20)


# Run the application
root = tk.Tk()
app = ElectricBillManagement(root)
root.mainloop()



if __name__ == "__main__":
    root = tk.Tk()
    app = ElectricBillManagement(root)
    root.mainloop()
