import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime

class ContactDialog:
    def __init__(self, parent, title, contact=None, view_mode=False):
        self.top = tk.Toplevel(parent)
        self.top.title(title)
        self.top.geometry("500x400")
        self.top.configure(bg='#f5f5f5')
        self.top.resizable(False, False)
        self.top.grab_set()  # Make dialog modal
        
        self.result = False
        self.view_mode = view_mode
        
        # Initialize variables
        self.name_var = tk.StringVar()
        self.phone_var = tk.StringVar()
        self.email_var = tk.StringVar()
        
        # If editing existing contact, populate fields
        if contact:
            self.name_var.set(contact.get('name', ''))
            self.phone_var.set(contact.get('phone', ''))
            self.email_var.set(contact.get('email', ''))
            self.address_text = contact.get('address', '')
        else:
            self.address_text = ''
        
        # Setup the UI
        self.setup_ui()
        
        # If in view mode, disable all fields
        if view_mode:
            self.set_view_mode()
    
    def setup_ui(self):
        # Main frame
        main_frame = tk.Frame(self.top, bg='#f5f5f5', padx=20, pady=20)
        main_frame.pack(fill='both', expand=True)
        
        # Name field
        tk.Label(main_frame, text="Name:*", font=('Arial', 12), bg='#f5f5f5').grid(row=0, column=0, sticky='w', pady=5)
        name_entry = tk.Entry(main_frame, textvariable=self.name_var, font=('Arial', 12), width=30)
        name_entry.grid(row=0, column=1, sticky='w', pady=5, padx=(10, 0))
        
        # Phone field
        tk.Label(main_frame, text="Phone:*", font=('Arial', 12), bg='#f5f5f5').grid(row=1, column=0, sticky='w', pady=5)
        phone_entry = tk.Entry(main_frame, textvariable=self.phone_var, font=('Arial', 12), width=30)
        phone_entry.grid(row=1, column=1, sticky='w', pady=5, padx=(10, 0))
        
        # Email field
        tk.Label(main_frame, text="Email:", font=('Arial', 12), bg='#f5f5f5').grid(row=2, column=0, sticky='w', pady=5)
        email_entry = tk.Entry(main_frame, textvariable=self.email_var, font=('Arial', 12), width=30)
        email_entry.grid(row=2, column=1, sticky='w', pady=5, padx=(10, 0))
        
        # Address field
        tk.Label(main_frame, text="Address:", font=('Arial', 12), bg='#f5f5f5').grid(row=3, column=0, sticky='nw', pady=5)
        self.address_textbox = tk.Text(main_frame, height=5, width=30, font=('Arial', 10))
        self.address_textbox.grid(row=3, column=1, sticky='w', pady=5, padx=(10, 0))
        self.address_textbox.insert('1.0', self.address_text)
        
        # Button frame
        button_frame = tk.Frame(main_frame, bg='#f5f5f5')
        button_frame.grid(row=4, column=0, columnspan=2, pady=20)
        
        if not self.view_mode:
            ok_button = tk.Button(button_frame, text="OK", command=self.ok, 
                                 bg='#27ae60', fg='white', font=('Arial', 12))
            ok_button.pack(side='left', padx=10)
        
        cancel_button = tk.Button(button_frame, text="Cancel", command=self.cancel,
                                 bg='#95a5a6', fg='white', font=('Arial', 12))
        cancel_button.pack(side='left', padx=10)
        
        # Make dialog modal
        self.top.transient(self.top.master)
        self.top.focus_force()
        
        # Bind Enter key to OK and Escape to Cancel
        self.top.bind('<Return>', lambda e: self.ok())
        self.top.bind('<Escape>', lambda e: self.cancel())
    
    def set_view_mode(self):
        # Disable all fields
        for child in self.top.winfo_children():
            if isinstance(child, tk.Entry):
                child.config(state='readonly')
            elif isinstance(child, tk.Text):
                child.config(state='disabled')
    
    def ok(self):
        # Validate required fields
        if not self.name_var.get().strip() or not self.phone_var.get().strip():
            messagebox.showwarning("Warning", "Name and phone number are required!")
            return
            
        self.result = True
        self.top.destroy()
    
    def cancel(self):
        self.result = False
        self.top.destroy()
        
    def get_address(self):
        return self.address_textbox.get("1.0", tk.END).strip()


class ContactManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Contact Manager")
        self.root.geometry("900x600")
        self.root.configure(bg='#f5f5f5')
        self.root.resizable(True, True)
        
        # Initialize contacts list
        self.contacts = []
        self.filtered_contacts = []
        
        # Load previous contacts if available
        self.load_contacts()
        
        # Search variable
        self.search_var = tk.StringVar()
        self.search_var.trace('w', self.filter_contacts)
        
        # Setup the UI
        self.setup_ui()
        
        # Update contact list
        self.update_contact_list()
    
    def setup_ui(self):
        # Header frame
        header_frame = tk.Frame(self.root, bg='#2c3e50', height=80)
        header_frame.pack(fill='x', padx=10, pady=10)
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(header_frame, text="Contact Manager", font=('Arial', 24, 'bold'), 
                              fg='white', bg='#2c3e50')
        title_label.pack(side='left', padx=20)
        
        # Add some sample data button for testing
        sample_btn = tk.Button(header_frame, text="Add Sample Data", command=self.add_sample_data,
                              bg='#3498db', fg='white', font=('Arial', 10))
        sample_btn.pack(side='right', padx=10)
        
        # Search frame
        search_frame = tk.Frame(self.root, bg='#f5f5f5')
        search_frame.pack(fill='x', padx=20, pady=10)
        
        tk.Label(search_frame, text="Search:", font=('Arial', 12), bg='#f5f5f5').pack(side='left')
        
        search_entry = tk.Entry(search_frame, textvariable=self.search_var, font=('Arial', 12), width=30)
        search_entry.pack(side='left', padx=10)
        
        clear_search_btn = tk.Button(search_frame, text="Clear", command=self.clear_search,
                                    bg='#95a5a6', fg='white', font=('Arial', 10))
        clear_search_btn.pack(side='left', padx=5)
        
        # Buttons frame
        buttons_frame = tk.Frame(self.root, bg='#f5f5f5')
        buttons_frame.pack(fill='x', padx=20, pady=(0, 10))
        
        add_button = tk.Button(buttons_frame, text="Add Contact", command=self.add_contact,
                              bg='#27ae60', fg='white', font=('Arial', 12, 'bold'))
        add_button.pack(side='left', padx=5)
        
        view_button = tk.Button(buttons_frame, text="View Details", command=self.view_contact,
                               bg='#3498db', fg='white', font=('Arial', 12))
        view_button.pack(side='left', padx=5)
        
        edit_button = tk.Button(buttons_frame, text="Edit Contact", command=self.edit_contact,
                               bg='#f39c12', fg='white', font=('Arial', 12))
        edit_button.pack(side='left', padx=5)
        
        delete_button = tk.Button(buttons_frame, text="Delete Contact", command=self.delete_contact,
                                 bg='#e74c3c', fg='white', font=('Arial', 12))
        delete_button.pack(side='left', padx=5)
        
        # Contacts frame
        contacts_frame = tk.LabelFrame(self.root, text="Contacts", font=('Arial', 14, 'bold'),
                                      bg='#f5f5f5', padx=10, pady=10)
        contacts_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Create a treeview with scrollbar
        tree_frame = tk.Frame(contacts_frame)
        tree_frame.pack(fill='both', expand=True)
        
        columns = ('name', 'phone', 'email')
        self.tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=15)
        
        # Define headings
        self.tree.heading('name', text='Name', command=lambda: self.sort_by_column('name', False))
        self.tree.heading('phone', text='Phone', command=lambda: self.sort_by_column('phone', False))
        self.tree.heading('email', text='Email', command=lambda: self.sort_by_column('email', False))
        
        # Define columns
        self.tree.column('name', width=200, anchor='w')
        self.tree.column('phone', width=150, anchor='w')
        self.tree.column('email', width=250, anchor='w')
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Bind double click to view contact
        self.tree.bind('<Double-1>', lambda e: self.view_contact())
        
        # Status bar
        self.status_var = tk.StringVar()
        self.update_status_bar()
        
        status_bar = tk.Label(self.root, textvariable=self.status_var, bd=1, relief=tk.SUNKEN, 
                             anchor=tk.W, bg='#E0E0E0', font=('Arial', 10))
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def add_sample_data(self):
        """Add some sample contacts for testing"""
        sample_contacts = [
            {
                'id': 1,
                'name': 'John Doe',
                'phone': '555-1234',
                'email': 'john@example.com',
                'address': '123 Main St, Anytown',
                'date_added': datetime.now().strftime("%Y-%m-%d %H:%M")
            },
            {
                'id': 2,
                'name': 'Jane Smith',
                'phone': '555-5678',
                'email': 'jane@example.com',
                'address': '456 Oak Ave, Somewhere',
                'date_added': datetime.now().strftime("%Y-%m-%d %H:%M")
            },
            {
                'id': 3,
                'name': 'Bob Johnson',
                'phone': '555-9012',
                'email': 'bob@example.com',
                'address': '789 Pine Rd, Nowhere',
                'date_added': datetime.now().strftime("%Y-%m-%d %H:%M")
            }
        ]
        
        self.contacts = sample_contacts
        self.filtered_contacts = self.contacts
        self.update_contact_list()
        self.save_contacts()
        messagebox.showinfo("Sample Data", "Sample contacts added successfully!")
    
    def add_contact(self):
        # Create a dialog for adding a new contact
        dialog = ContactDialog(self.root, "Add New Contact")
        self.root.wait_window(dialog.top)
        
        if dialog.result:
            # Find the next available ID
            next_id = max([c['id'] for c in self.contacts], default=0) + 1
            
            contact = {
                'id': next_id,
                'name': dialog.name_var.get().strip(),
                'phone': dialog.phone_var.get().strip(),
                'email': dialog.email_var.get().strip(),
                'address': dialog.get_address(),
                'date_added': datetime.now().strftime("%Y-%m-%d %H:%M")
            }
            
            # Validate required fields
            if not contact['name'] or not contact['phone']:
                messagebox.showwarning("Warning", "Name and phone number are required!")
                return
                
            self.contacts.append(contact)
            self.filtered_contacts = self.contacts
            self.update_contact_list()
            self.save_contacts()
            messagebox.showinfo("Success", "Contact added successfully!")
    
    def view_contact(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a contact to view!")
            return
            
        try:
            contact_id = int(selected[0])
            contact = next((c for c in self.contacts if c['id'] == contact_id), None)
            
            if contact:
                # Create a view dialog
                dialog = ContactDialog(self.root, "View Contact: " + contact['name'], contact, view_mode=True)
                self.root.wait_window(dialog.top)
            else:
                messagebox.showerror("Error", "Contact not found!")
        except ValueError:
            messagebox.showerror("Error", "Invalid contact selection!")
    
    def edit_contact(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a contact to edit!")
            return
            
        try:
            contact_id = int(selected[0])
            contact = next((c for c in self.contacts if c['id'] == contact_id), None)
            
            if contact:
                # Create an edit dialog
                dialog = ContactDialog(self.root, "Edit Contact: " + contact['name'], contact)
                self.root.wait_window(dialog.top)
                
                if dialog.result:
                    contact['name'] = dialog.name_var.get().strip()
                    contact['phone'] = dialog.phone_var.get().strip()
                    contact['email'] = dialog.email_var.get().strip()
                    contact['address'] = dialog.get_address()
                    
                    # Validate required fields
                    if not contact['name'] or not contact['phone']:
                        messagebox.showwarning("Warning", "Name and phone number are required!")
                        return
                        
                    self.update_contact_list()
                    self.save_contacts()
                    messagebox.showinfo("Success", "Contact updated successfully!")
            else:
                messagebox.showerror("Error", "Contact not found!")
        except ValueError:
            messagebox.showerror("Error", "Invalid contact selection!")
    
    def delete_contact(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a contact to delete!")
            return
            
        try:
            contact_id = int(selected[0])
            contact = next((c for c in self.contacts if c['id'] == contact_id), None)
            
            if contact:
                if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete {contact['name']}?"):
                    self.contacts = [c for c in self.contacts if c['id'] != contact_id]
                    self.filtered_contacts = self.contacts
                    self.update_contact_list()
                    self.save_contacts()
                    messagebox.showinfo("Success", "Contact deleted successfully!")
            else:
                messagebox.showerror("Error", "Contact not found!")
        except ValueError:
            messagebox.showerror("Error", "Invalid contact selection!")
    
    def filter_contacts(self, *args):
        search_term = self.search_var.get().lower()
        
        if not search_term:
            self.filtered_contacts = self.contacts
        else:
            self.filtered_contacts = [
                c for c in self.contacts 
                if search_term in c['name'].lower() 
                or search_term in c['phone'].lower()
                or (c['email'] and search_term in c['email'].lower())
            ]
        
        self.update_contact_list()
    
    def clear_search(self):
        self.search_var.set("")
        self.filtered_contacts = self.contacts
        self.update_contact_list()
    
    def update_contact_list(self):
        # Clear the treeview
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Add contacts to treeview
        for contact in self.filtered_contacts:
            self.tree.insert('', tk.END, values=(
                contact['name'], 
                contact['phone'], 
                contact.get('email', '')  # Use get to handle missing email field
            ), iid=contact['id'])
        
        self.update_status_bar()
    
    def update_status_bar(self):
        total_contacts = len(self.contacts)
        filtered_contacts = len(self.filtered_contacts)
        
        if total_contacts == filtered_contacts:
            self.status_var.set(f"Total Contacts: {total_contacts}")
        else:
            self.status_var.set(f"Showing {filtered_contacts} of {total_contacts} contacts")
    
    def sort_by_column(self, column, reverse):
        # Get all values from the treeview
        items = [(self.tree.set(item, column), item) for item in self.tree.get_children('')]
        
        # Sort the items
        items.sort(reverse=reverse)
        
        # Rearrange items in sorted positions
        for index, (values, item) in enumerate(items):
            self.tree.move(item, '', index)
        
        # Reverse sort next time
        self.tree.heading(column, command=lambda: self.sort_by_column(column, not reverse))
    
    def save_contacts(self):
        try:
            with open('contacts.json', 'w') as f:
                json.dump(self.contacts, f, indent=2)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save contacts: {str(e)}")
    
    def load_contacts(self):
        if os.path.exists('contacts.json'):
            try:
                with open('contacts.json', 'r') as f:
                    self.contacts = json.load(f)
                self.filtered_contacts = self.contacts
                print(f"Loaded {len(self.contacts)} contacts")  # Debug print
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load contacts: {str(e)}")
                self.contacts = []
                self.filtered_contacts = []
        else:
            self.contacts = []
            self.filtered_contacts = []
            print("No contacts file found")  # Debug print

def main():
    root = tk.Tk()
    app = ContactManager(root)
    root.mainloop()

if __name__ == "__main__":
    main()
