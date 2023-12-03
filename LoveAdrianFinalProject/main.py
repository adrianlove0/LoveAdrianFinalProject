import tkinter as tk
from tkinter import messagebox
import json


class AccountManager:
    def __init__(self):
        # File to store account information in JSON format
        self.accounts = None
        self.accounts_file = "accounts.json"
        # Current user logged in
        self.current_user = None
        # Load existing accounts from the JSON file
        self.load_accounts()

    def load_accounts(self):
        """Load existing accounts from the JSON file."""
        try:
            with open(self.accounts_file, 'r') as file:
                self.accounts = json.load(file)
        except FileNotFoundError:
            # If the file doesn't exist, initialize an empty dictionary
            self.accounts = {}

    def save_accounts(self):
        """Save accounts to the JSON file."""
        with open(self.accounts_file, 'w') as file:
            json.dump(self.accounts, file, indent=2)

    def register_account(self, username, password, info):
        """Register a new account."""
        if username in self.accounts:
            # Display an error message if the username already exists
            messagebox.showerror("Error", "Username already exists")
        else:
            # Store username, password, and user information in the accounts dictionary
            self.accounts[username] = {"password": password, "info": info}
            # Save the updated accounts to the file
            self.save_accounts()
            # Display a success message
            messagebox.showinfo("Success", "Account registered successfully")

    def login(self, username, password):
        """Log in to an existing account."""
        if username in self.accounts and self.accounts[username]["password"] == password:
            # Set the current user upon successful login
            self.current_user = username
            return True
        else:
            # Display an error message for invalid username or password
            messagebox.showerror("Error", "Invalid username or password")
            return False

    def logout(self):
        """Log out the current user."""
        # Set the current user to None
        self.current_user = None

    def get_user_info(self):
        """Retrieve user information for the current user."""
        if self.current_user:
            return self.accounts[self.current_user]["info"]
        return {}


class App:
    def __init__(self, root):
        # Initialize the main application window
        self.username_var = None
        self.password_var = None
        self.root = root
        self.root.title("Account Management System")
        # Create an instance of the AccountManager class
        self.account_manager = AccountManager()

        # Start with the login window
        self.login_window()

    def login_window(self):
        """Create the login window."""
        self.clear_window()
        # Variables to store the entered username and password
        self.username_var = tk.StringVar()
        self.password_var = tk.StringVar()

        tk.Label(self.root, text="Username:").pack()
        tk.Entry(self.root, textvariable=self.username_var).pack()

        tk.Label(self.root, text="Password:").pack()
        tk.Entry(self.root, textvariable=self.password_var, show="*").pack()

        tk.Button(self.root, text="Login", command=self.login).pack()
        tk.Button(self.root, text="Register", command=self.register).pack()

    def home_window(self):
        """Create the home window after successful login."""
        self.clear_window()

        tk.Label(self.root, text=f"Welcome, {self.account_manager.current_user}!").pack()

        tk.Button(self.root, text="View Personal Information", command=self.view_personal_info).pack()
        tk.Button(self.root, text="Logout", command=self.logout).pack()

    def personal_info_window(self):
        """Create the personal information window."""
        self.clear_window()

        user_info = self.account_manager.get_user_info()
        tk.Label(self.root, text="Personal Information").pack()

        for key, value in user_info.items():
            tk.Label(self.root, text=f"{key.capitalize()}: {value}").pack()

        tk.Button(self.root, text="Back", command=self.home_window).pack()

    def clear_window(self):
        """Clear all widgets from the current window."""
        for widget in self.root.winfo_children():
            widget.destroy()

    def login(self):
        """Attempt to log in with the provided credentials."""
        username = self.username_var.get()
        password = self.password_var.get()

        if self.account_manager.login(username, password):
            self.home_window()
        else:
            self.clear_fields()

    def register(self):
        """Create the registration window."""
        username = self.username_var.get()
        password = self.password_var.get()

        info_window = tk.Toplevel(self.root)
        info_window.title("User Information")

        tk.Label(info_window, text="User Information").pack()

        tk.Label(info_window, text="Name:").pack()
        name_var = tk.StringVar()
        tk.Entry(info_window, textvariable=name_var).pack()

        tk.Label(info_window, text="Age:").pack()
        age_var = tk.StringVar()
        tk.Entry(info_window, textvariable=age_var).pack()

        tk.Label(info_window, text="Gender:").pack()
        gender_var = tk.StringVar()
        tk.Entry(info_window, textvariable=gender_var).pack()

        tk.Label(info_window, text="Birthday:").pack()
        birthday_var = tk.StringVar()
        tk.Entry(info_window, textvariable=birthday_var).pack()

        tk.Label(info_window, text="Address:").pack()
        address_var = tk.StringVar()
        tk.Entry(info_window, textvariable=address_var).pack()

        tk.Label(info_window, text="Phone Number:").pack()
        phone_var = tk.StringVar()
        tk.Entry(info_window, textvariable=phone_var).pack()

        tk.Button(info_window, text="Register", command=lambda: self.account_manager.register_account(
            username, password, {
                "Name": name_var.get(),
                "Age": age_var.get(),
                "Gender": gender_var.get(),
                "Birthday": birthday_var.get(),
                "Address": address_var.get(),
                "Phone Number": phone_var.get()
            })).pack()

    def view_personal_info(self):
        """View the personal information of the logged-in user."""
        if self.account_manager.current_user:
            self.personal_info_window()
        else:
            messagebox.showerror("Error", "Please log in first")

    def logout(self):
        """Log out the current user and return to the login window."""
        self.account_manager.logout()
        self.clear_fields()
        self.login_window()

    def clear_fields(self):
        """Clear the username and password fields."""
        self.username_var.set("")
        self.password_var.set("")


if __name__ == "__main__":
    # Create the main Tkinter window and run the application
    root = tk.Tk()
    app = App(root)
    root.mainloop()
