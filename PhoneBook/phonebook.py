"""
Program: phonebook.py
Author: Adrian Love
Last date modified: 12/16/2023

The purpose of this program is to act as a digital phone book. You can add, remove, and edit
contacts in the book. You also have the option to add a photo to your contact.
"""


import os
import tkinter as tk
from tkinter import messagebox, filedialog
import json
from PIL import Image, ImageTk


class PhoneBookApp:
    def __init__(self, root):
        """
        Initialize the PhoneBookApp.

        Parameters:
            - root (tk.Tk): The root Tkinter window.
        """
        # Declaring variables at program startup
        self.contact_listbox = None
        self.add_button = None
        self.edit_button = None
        self.remove_button = None
        self.show_button = None
        self.name_entry = None
        self.phone_entry = None
        self.address_entry = None
        self.photo_path_entry = None
        self.edit_name_entry = None
        self.edit_phone_entry = None
        self.edit_address_entry = None

        self.root = root  # Root Tkinter window
        self.root.title("Phone Book App")
        self.contacts = {}  # Dictionary to store contact information
        self.load_data()  # Load existing contacts

        self.create_gui()  # Create the graphical user interface (GUI) for the application

    def create_gui(self):
        """
        Create the graphical user interface (GUI) for the application.
        """
        # Contact Listbox
        self.contact_listbox = tk.Listbox(self.root, selectmode=tk.SINGLE)
        self.contact_listbox.pack(side=tk.LEFT, padx=10, pady=10)

        # Refresh contact list
        self.refresh_contact_list()

        # Buttons for actions
        self.add_button = tk.Button(self.root, text="Add Contact", command=self.add_contact_window)
        self.add_button.pack(side=tk.TOP)

        self.edit_button = tk.Button(self.root, text="Edit Contact", command=self.edit_contact_window)
        self.edit_button.pack(side=tk.TOP)

        self.remove_button = tk.Button(self.root, text="Remove Contact", command=self.remove_contact)
        self.remove_button.pack(side=tk.TOP)

        self.show_button = tk.Button(self.root, text="Show Contact", command=self.show_contact_window)
        self.show_button.pack(side=tk.TOP)

    def add_contact_window(self):
        """
        Create a new window for adding a contact.
        """
        add_window = tk.Toplevel(self.root)
        add_window.title("Add Contact")

        # Entry fields for contact information
        name_label = tk.Label(add_window, text="Name:")
        name_label.grid(row=0, column=0)
        self.name_entry = tk.Entry(add_window)  # Entry for the contact's name
        self.name_entry.grid(row=0, column=1)

        phone_label = tk.Label(add_window, text="Phone:")
        phone_label.grid(row=1, column=0)
        self.phone_entry = tk.Entry(add_window)  # Entry for the contact's phone number
        self.phone_entry.grid(row=1, column=1)

        address_label = tk.Label(add_window, text="Address:")
        address_label.grid(row=2, column=0)
        self.address_entry = tk.Entry(add_window)  # Entry for the contact's address
        self.address_entry.grid(row=2, column=1)

        photo_label = tk.Label(add_window, text="Photo:")
        photo_label.grid(row=3, column=0)
        self.photo_path_entry = tk.Entry(add_window)  # Entry for the photo path
        self.photo_path_entry.grid(row=3, column=1)
        photo_button = tk.Button(add_window, text="Browse", command=self.browse_photo)
        photo_button.grid(row=3, column=2)

        # Button to add the contact
        add_button = tk.Button(add_window, text="Add", command=self.add_contact)
        add_button.grid(row=4, column=0, columnspan=2, pady=10)

    def edit_contact_window(self):
        """
        Create a new window for editing a contact.
        """
        selected_index = self.contact_listbox.curselection()
        if not selected_index:
            messagebox.showinfo("Error", "Please select a contact to edit.")
            return

        selected_contact = self.contacts[self.contact_listbox.get(selected_index)]
        edit_window = tk.Toplevel(self.root)
        edit_window.title("Edit Contact")

        # Entry fields for editing contact information
        name_label = tk.Label(edit_window, text="Name:")
        name_label.grid(row=0, column=0)
        self.edit_name_entry = tk.Entry(edit_window)  # Entry for the edited contact's name
        self.edit_name_entry.insert(0, selected_contact["Name"])
        self.edit_name_entry.grid(row=0, column=1)

        phone_label = tk.Label(edit_window, text="Phone:")
        phone_label.grid(row=1, column=0)
        self.edit_phone_entry = tk.Entry(edit_window)  # Entry for the edited contact's phone number
        self.edit_phone_entry.insert(0, selected_contact["Phone"])
        self.edit_phone_entry.grid(row=1, column=1)

        address_label = tk.Label(edit_window, text="Address:")
        address_label.grid(row=2, column=0)
        self.edit_address_entry = tk.Entry(edit_window)  # Entry for the edited contact's address
        self.edit_address_entry.insert(0, selected_contact["Address"])
        self.edit_address_entry.grid(row=2, column=1)

        # Button to save the edited contact
        save_button = tk.Button(edit_window, text="Save", command=lambda: self.save_contact(selected_index))
        save_button.grid(row=3, column=0, columnspan=2, pady=10)

    def show_contact_window(self):
        selected_index = self.contact_listbox.curselection()
        if not selected_index:
            messagebox.showinfo("Error", "Please select a contact to show.")
            return

        selected_contact = self.contacts[self.contact_listbox.get(selected_index)]
        show_window = tk.Toplevel(self.root)
        show_window.title("Contact Information")

        # Display contact information
        name_label = tk.Label(show_window, text=f"Name: {selected_contact['Name']}")
        name_label.pack()

        phone_label = tk.Label(show_window, text=f"Phone: {selected_contact['Phone']}")
        phone_label.pack()

        address_label = tk.Label(show_window, text=f"Address: {selected_contact['Address']}")
        address_label.pack()

        # Display photo if available
        if 'Photo' in selected_contact:
            photo_path = selected_contact['Photo']
            if photo_path and os.path.exists(photo_path):
                try:
                    photo = Image.open(photo_path)
                    photo = photo.resize((150, 150), Image.BICUBIC)
                    photo = ImageTk.PhotoImage(photo)

                    photo_label = tk.Label(show_window, image=photo)
                    photo_label.image = photo
                    photo_label.pack()
                except Exception as e:
                    messagebox.showinfo("Error", f"Error loading photo: {str(e)}")
            else:
                # Handle the case where the photo path is empty or the file does not exist
                default_photo_label = tk.Label(show_window, text="No Photo Available")
                default_photo_label.pack()

    def browse_photo(self):
        """
        Open a file dialog to browse and select a photo file.
        """
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
        self.photo_path_entry.delete(0, tk.END)
        self.photo_path_entry.insert(0, file_path)

    def add_contact(self):
        """
        Add a new contact to the phone book.
        """
        name = self.name_entry.get()
        phone = self.phone_entry.get()
        address = self.address_entry.get()
        photo_path = self.photo_path_entry.get()

        if name and phone:
            contact = {"Name": name, "Phone": phone, "Address": address, "Photo": photo_path}
            self.contacts[name] = contact
            self.refresh_contact_list()
            self.save_data()
        else:
            messagebox.showinfo("Error", "Name and phone number are required.")

    def save_contact(self, selected_index):
        """
        Save the edited contact information.
        """
        selected_contact_name = self.contact_listbox.get(selected_index)
        edited_contact = {
            "Name": self.edit_name_entry.get(),
            "Phone": self.edit_phone_entry.get(),
            "Address": self.edit_address_entry.get()
        }

        self.contacts[selected_contact_name] = edited_contact
        self.refresh_contact_list()
        self.save_data()

    def remove_contact(self):
        """
        Remove the selected contact from the phone book.
        """
        selected_index = self.contact_listbox.curselection()
        if not selected_index:
            messagebox.showinfo("Error", "Please select a contact to remove.")
            return

        selected_contact_name = self.contact_listbox.get(selected_index)
        del self.contacts[selected_contact_name]
        self.refresh_contact_list()
        self.save_data()

    def refresh_contact_list(self):
        """
        Refresh the contact list in the GUI.
        """
        self.contact_listbox.delete(0, tk.END)

        # Sort contact names alphabetically
        sorted_contact_names = sorted(self.contacts.keys())

        # Insert sorted contact names into the listbox
        for contact_name in sorted_contact_names:
            self.contact_listbox.insert(tk.END, contact_name)

    def load_data(self):
        """
        Load existing contacts from a JSON file.
        """
        try:
            with open("phonebook_data.json", "r") as file:
                self.contacts = json.load(file)
        except FileNotFoundError:
            pass

    def save_data(self):
        """
        Save the current contacts to a JSON file.
        """
        with open("phonebook_data.json", "w") as file:
            json.dump(self.contacts, file, indent=2)


if __name__ == "__main__":
    # Main program entry point
    root = tk.Tk()
    app = PhoneBookApp(root)
    root.mainloop()
