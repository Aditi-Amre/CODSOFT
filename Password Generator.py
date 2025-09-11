import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import random
import string

class PasswordGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Password Generator")
        self.root.geometry("500x500")
        self.root.resizable(False, False)
        self.root.configure(bg='#f0f0f0')
        
        # Variables
        self.password_length = tk.IntVar(value=12)
        self.include_uppercase = tk.BooleanVar(value=True)
        self.include_lowercase = tk.BooleanVar(value=True)
        self.include_digits = tk.BooleanVar(value=True)
        self.include_special = tk.BooleanVar(value=True)
        
        # Create UI
        self.create_widgets()
        
    def create_widgets(self):
        # Title
        title_label = tk.Label(
            self.root, 
            text="Password Generator", 
            font=('Arial', 18, 'bold'),
            bg='#f0f0f0',
            fg='#2c3e50'
        )
        title_label.pack(pady=15)
        
        # Length selection frame
        length_frame = tk.Frame(self.root, bg='#f0f0f0')
        length_frame.pack(pady=10, padx=20, fill="x")
        
        length_label = tk.Label(
            length_frame, 
            text="Password Length:", 
            font=('Arial', 12),
            bg='#f0f0f0'
        )
        length_label.pack(side=tk.LEFT)
        
        length_scale = tk.Scale(
            length_frame,
            from_=6,
            to=30,
            orient=tk.HORIZONTAL,
            variable=self.password_length,
            bg='#f0f0f0',
            highlightthickness=0
        )
        length_scale.pack(side=tk.RIGHT, fill="x", expand=True)
        
        # Complexity options frame
        options_frame = tk.LabelFrame(
            self.root, 
            text="Password Complexity",
            font=('Arial', 12, 'bold'),
            bg='#f0f0f0',
            padx=10,
            pady=10
        )
        options_frame.pack(pady=10, padx=20, fill="x")
        
        tk.Checkbutton(
            options_frame, 
            text="Uppercase Letters (A-Z)", 
            variable=self.include_uppercase,
            font=('Arial', 10),
            bg='#f0f0f0',
            activebackground='#f0f0f0'
        ).pack(anchor="w", pady=2)
        
        tk.Checkbutton(
            options_frame, 
            text="Lowercase Letters (a-z)", 
            variable=self.include_lowercase,
            font=('Arial', 10),
            bg='#f0f0f0',
            activebackground='#f0f0f0'
        ).pack(anchor="w", pady=2)
        
        tk.Checkbutton(
            options_frame, 
            text="Digits (0-9)", 
            variable=self.include_digits,
            font=('Arial', 10),
            bg='#f0f0f0',
            activebackground='#f0f0f0'
        ).pack(anchor="w", pady=2)
        
        tk.Checkbutton(
            options_frame, 
            text="Special Characters (!@#$%^&*)", 
            variable=self.include_special,
            font=('Arial', 10),
            bg='#f0f0f0',
            activebackground='#f0f0f0'
        ).pack(anchor="w", pady=2)
        
        # Generate button
        generate_btn = tk.Button(
            self.root,
            text="Generate Password",
            command=self.generate_password,
            font=('Arial', 12, 'bold'),
            bg='#3498db',
            fg='white',
            padx=20,
            pady=8,
            cursor='hand2'
        )
        generate_btn.pack(pady=15)
        
        # Generated password display
        result_frame = tk.LabelFrame(
            self.root, 
            text="Generated Password",
            font=('Arial', 12, 'bold'),
            bg='#f0f0f0',
            padx=10,
            pady=10
        )
        result_frame.pack(pady=10, padx=20, fill="both", expand=True)
        
        # Scrollable text area for password
        self.password_display = scrolledtext.ScrolledText(
            result_frame,
            height=4,
            width=50,
            font=('Courier', 12),
            wrap=tk.WORD,
            padx=10,
            pady=10
        )
        self.password_display.pack(fill="both", expand=True)
        self.password_display.config(state=tk.DISABLED)
        
        # Copy button
        copy_btn = tk.Button(
            self.root,
            text="Copy to Clipboard",
            command=self.copy_to_clipboard,
            font=('Arial', 10),
            bg='#2ecc71',
            fg='white',
            padx=15,
            pady=5
        )
        copy_btn.pack(pady=10)
        
        # Strength indicator
        self.strength_label = tk.Label(
            self.root,
            text="Password Strength: Not Generated",
            font=('Arial', 10),
            bg='#f0f0f0',
            fg='#7f8c8d'
        )
        self.strength_label.pack(pady=5)
        
    def generate_password(self):
        # Check if at least one character set is selected
        if not (self.include_uppercase.get() or self.include_lowercase.get() or 
                self.include_digits.get() or self.include_special.get()):
            messagebox.showerror("Error", "Please select at least one character type!")
            return
        
        # Define character sets
        char_sets = []
        if self.include_uppercase.get():
            char_sets.append(string.ascii_uppercase)
        if self.include_lowercase.get():
            char_sets.append(string.ascii_lowercase)
        if self.include_digits.get():
            char_sets.append(string.digits)
        if self.include_special.get():
            char_sets.append("!@#$%^&*")
        
        # Ensure we have at least one character from each selected set
        password = []
        for char_set in char_sets:
            password.append(random.choice(char_set))
        
        # Fill the rest of the password with random characters from all selected sets
        all_chars = ''.join(char_sets)
        for _ in range(self.password_length.get() - len(password)):
            password.append(random.choice(all_chars))
        
        # Shuffle the password
        random.shuffle(password)
        password = ''.join(password)
        
        # Display the password
        self.password_display.config(state=tk.NORMAL)
        self.password_display.delete(1.0, tk.END)
        self.password_display.insert(tk.END, password)
        self.password_display.config(state=tk.DISABLED)
        
        # Update strength indicator
        self.update_strength_indicator(password)
    
    def update_strength_indicator(self, password):
        # Simple password strength calculation
        strength = 0
        length = len(password)
        
        # Length factor
        if length >= 12:
            strength += 2
        elif length >= 8:
            strength += 1
            
        # Character diversity factor
        has_upper = any(c in string.ascii_uppercase for c in password)
        has_lower = any(c in string.ascii_lowercase for c in password)
        has_digit = any(c in string.digits for c in password)
        has_special = any(c in "!@#$%^&*" for c in password)
        
        diversity = sum([has_upper, has_lower, has_digit, has_special])
        strength += diversity
        
        # Set strength text and color
        if strength >= 5:
            text = "Password Strength: Very Strong"
            color = "#27ae60"
        elif strength >= 4:
            text = "Password Strength: Strong"
            color = "#2ecc71"
        elif strength >= 3:
            text = "Password Strength: Medium"
            color = "#f39c12"
        else:
            text = "Password Strength: Weak"
            color = "#e74c3c"
            
        self.strength_label.config(text=text, fg=color)
    
    def copy_to_clipboard(self):
        password = self.password_display.get(1.0, tk.END).strip()
        if password:
            # Create a temporary widget to copy to clipboard
            temp = tk.Tk()
            temp.withdraw()
            temp.clipboard_clear()
            temp.clipboard_append(password)
            temp.update()
            temp.destroy()
            
            messagebox.showinfo("Success", "Password copied to clipboard!")
        else:
            messagebox.showwarning("Warning", "No password to copy!")

if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordGenerator(root)
    root.mainloop()
