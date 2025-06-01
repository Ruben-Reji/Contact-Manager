import tkinter as tk
from tkinter import messagebox, simpledialog
import json
import os

CONTACTS_FILE = "contacts.json"

# Load or initialize contacts
def load_contacts():
    if os.path.exists(CONTACTS_FILE):
        with open(CONTACTS_FILE, "r") as file:
            return json.load(file)
    return []

def save_contacts(contacts):
    with open(CONTACTS_FILE, "w") as file:
        json.dump(contacts, file, indent=4)

class ContactManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Contact Manager")
        self.contacts = load_contacts()

        self.create_widgets()
        self.refresh_contact_list()

    def create_widgets(self):
        self.listbox = tk.Listbox(self.root, width=50)
        self.listbox.pack(padx=10, pady=10)

        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=5)

        tk.Button(btn_frame, text="Add Contact", command=self.add_contact).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Edit Contact", command=self.edit_contact).grid(row=0, column=1, padx=5)
        tk.Button(btn_frame, text="Delete Contact", command=self.delete_contact).grid(row=0, column=2, padx=5)

    def refresh_contact_list(self):
        self.listbox.delete(0, tk.END)
        for idx, contact in enumerate(self.contacts):
            self.listbox.insert(tk.END, f"{idx + 1}. {contact['name']} - {contact['phone']} - {contact['email']}")

    def add_contact(self):
        name = simpledialog.askstring("Name", "Enter name:")
        if not name:
            return
        phone = simpledialog.askstring("Phone", "Enter phone number:")
        email = simpledialog.askstring("Email", "Enter email address:")

        self.contacts.append({"name": name, "phone": phone, "email": email})
        save_contacts(self.contacts)
        self.refresh_contact_list()

    def edit_contact(self):
        selected = self.listbox.curselection()
        if not selected:
            messagebox.showwarning("Edit", "No contact selected.")
            return
        index = selected[0]
        contact = self.contacts[index]

        name = simpledialog.askstring("Edit Name", "Enter new name:", initialvalue=contact["name"])
        phone = simpledialog.askstring("Edit Phone", "Enter new phone number:", initialvalue=contact["phone"])
        email = simpledialog.askstring("Edit Email", "Enter new email:", initialvalue=contact["email"])

        self.contacts[index] = {"name": name, "phone": phone, "email": email}
        save_contacts(self.contacts)
        self.refresh_contact_list()

    def delete_contact(self):
        selected = self.listbox.curselection()
        if not selected:
            messagebox.showwarning("Delete", "No contact selected.")
            return
        index = selected[0]
        del self.contacts[index]
        save_contacts(self.contacts)
        self.refresh_contact_list()

# Run the app
if __name__ == "__main__":
    root = tk.Tk()
    app = ContactManagerApp(root)
    root.mainloop()
