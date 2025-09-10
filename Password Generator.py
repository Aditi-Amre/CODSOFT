import tkinter as tk
from tkinter import ttk, messagebox
import random
import string

class PasswordGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Password Generator")
        self.root.geometry("500x450")
        self.root.configure(bg='#f5f5f5')
        self.root.resizable(False, False)
        
        # Initialize variables
        self.password_length = tk.IntVar(value=12)
        self.include_uppercase = tk.BooleanVar(value=True)
        self.include_lowercase = tk.BooleanVar(value=True)
        self.include_digits = tk.BooleanVar(value=True)
        self.include_symbols = tk.BooleanVar(value=True)
        self.generated_password = tk.StringVar(value="Click 'Generate Password' to create a password")
        
        # Setup the UI
        self.setup_ui()
        
    def setup_ui(self):
        # Main frame
        main_frame = tk.Frame(self.root, bg='#f5f5f5', padx=20, pady=20)
        main_frame.pack(fill='both', expand=True)
        
        # Title
        title_label = tk.Label(main_frame, text="Password Generator", 
                              font=('Arial', 18, 'bold'), bg='#f5f5f5', fg='#2c3e50')
        title_label.pack(pady=(0, 20))
        
        # Length control frame
        length_frame = tk.Frame(main_frame, bg='#f5f5f5')
        length_frame.pack(fill='x', pady=(0, 15))
        
        tk.Label(length_frame, text="Password Length:", font=('Arial', 12), 
                bg='#f5f5f5').pack(side='left')
        
        length_scale = tk.Scale(length_frame, from_=6, to=32, orient=tk.HORIZONTAL,
                               variable=self.password_length, bg='#f5f5f5',
                               font=('Arial', 10), length=250, showvalue=True)
        length_scale.pack(side='right', padx=(20, 0))
        
        # Character sets frame
        sets_frame = tk.LabelFrame(main_frame, text="Character Sets", font=('Arial', 12, 'bold'),
                                  bg='#f5f5f5', padx=10, pady=10)
        sets_frame.pack(fill='x', pady=(0, 15))
        
        # Checkboxes for character sets
        tk.Checkbutton(sets_frame, text="Uppercase Letters (A-Z)", variable=self.include_uppercase,
                      font=('Arial', 10), bg='#f5f5f5').pack(anchor='w')
        tk.Checkbutton(sets_frame, text="Lowercase Letters (a-z)", variable=self.include_lowercase,
                      font=('Arial', 10), bg='#f5f5f5').pack(anchor='w')
        tk.Checkbutton(sets_frame, text="Digits (0-9)", variable=self.include_digits,
                      font=('Arial', 10), bg='#f5f5f5').pack(anchor='w')
        tk.Checkbutton(sets_frame, text="Symbols (!@#$%^&*)", variable=self.include_symbols,
                      font=('Arial', 10), bg='#f5f5f5').pack(anchor='w')
        
        # Generate button
        generate_btn = tk.Button(main_frame, text="Generate Password", command=self.generate_password,
                                bg='#3498db', fg='white', font=('Arial', 12, 'bold'),
                                padx=20, pady=8, relief='raised', bd=2)
        generate_btn.pack(pady=15)
        
        # Generated password frame
        password_frame = tk.Frame(main_frame, bg='#f5f5f5')
        password_frame.pack(fill='x', pady=(0, 15))
        
        tk.Label(password_frame, text="Generated Password:", font=('Arial', 12), 
                bg='#f5f5f5').pack(anchor='w')
        
        password_entry = tk.Entry(password_frame, textvariable=self.generated_password, 
                                 font=('Courier', 12), state='readonly', 
                                 readonlybackground='white', fg='#2c3e50', relief='sunken', bd=2)
        password_entry.pack(fill='x', pady=5, ipady=5)
        
        # Copy button
        copy_btn = tk.Button(main_frame, text="Copy to Clipboard", command=self.copy_to_clipboard,
                            bg='#2ecc71', fg='white', font=('Arial', 10),
                            padx=15, pady=5, relief='raised', bd=2)
        copy_btn.pack(pady=5)
        
        # Strength indicator
        self.strength_var = tk.StringVar(value="Password strength will appear here")
        strength_label = tk.Label(main_frame, textvariable=self.strength_var, 
                                 font=('Arial', 10), bg='#f5f5f5', fg='#7f8c8d')
        strength_label.pack(pady=5)
        
        # Footer
        footer_label = tk.Label(main_frame, text="© 2023 Password Generator", 
                               font=('Arial', 8), bg='#f5f5f5', fg='#95a5a6')
        footer_label.pack(side='bottom', pady=(20, 0))
    
    def generate_password(self):
        # Check if at least one character set is selected
        if not (self.include_uppercase.get() or self.include_lowercase.get() or 
                self.include_digits.get() or self.include_symbols.get()):
            messagebox.showwarning("Warning", "Please select at least one character set!")
            return
        
        # Define character sets
        char_pool = ""
        if self.include_uppercase.get():
            char_pool += string.ascii_uppercase
        if self.include_lowercase.get():
            char_pool += string.ascii_lowercase
        if self.include_digits.get():
            char_pool += string.digits
        if self.include_symbols.get():
            char_pool += "!@#$%^&*"
        
        # Generate password
        length = self.password_length.get()
        password = ''.join(random.choice(char_pool) for _ in range(length))
        
        # Update the password display
        self.generated_password.set(password)
        
        # Update strength indicator
        self.update_strength_indicator(password)
        
        # Show success message
        messagebox.showinfo("Success", "Password generated successfully!")
    
    def update_strength_indicator(self, password):
        # Simple password strength estimation
        length = len(password)
        has_upper = any(c.isupper() for c in password)
        has_lower = any(c.islower() for c in password)
        has_digit = any(c.isdigit() for c in password)
        has_symbol = any(not c.isalnum() for c in password)
        
        # Calculate strength score
        score = 0
        if length >= 12:
            score += 2
        elif length >= 8:
            score += 1
            
        if has_upper:
            score += 1
        if has_lower:
            score += 1
        if has_digit:
            score += 1
        if has_symbol:
            score += 1
        
        # Set strength text and color
        if score >= 6:
            self.strength_var.set("Very Strong (Excellent password)")
        elif score >= 5:
            self.strength_var.set("Strong (Good password)")
        elif score >= 4:
            self.strength_var.set("Medium (Adequate password)")
        elif score >= 3:
            self.strength_var.set("Weak (Consider improving)")
        else:
            self.strength_var.set("Very Weak (Not recommended)")
    
    def copy_to_clipboard(self):
        password = self.generated_password.get()
        if password and password != "Click 'Generate Password' to create a password":
            # For copying to clipboard without pyperclip
            self.root.clipboard_clear()
            self.root.clipboard_append(password)
            self.root.update()  # Now it stays on the clipboard after the window is closed
            messagebox.showinfo("Success", "Password copied to clipboard!")
        else:
            messagebox.showwarning("Warning", "No password to copy!")

# Create and run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordGenerator(root)
    root.mainloop()