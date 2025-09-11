import tkinter as tk
from tkinter import messagebox

class CalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple Calculator")
        self.root.geometry("300x400")
        self.root.resizable(False, False)
        
        # Variables
        self.current_input = ""
        self.first_number = None
        self.operation = None
        self.new_input = True
        
        # Create UI
        self.create_display()
        self.create_keypad()
        
    def create_display(self):
        # Display frame
        display_frame = tk.Frame(self.root, height=50)
        display_frame.pack(pady=10, padx=10, fill="x")
        
        # Display field
        self.display = tk.Entry(
            display_frame, 
            font=('Arial', 20), 
            bd=5, 
            relief=tk.RIDGE, 
            justify=tk.RIGHT,
            state='readonly'
        )
        self.display.pack(fill="x", ipady=10)
        
    def create_keypad(self):
        # Keypad frame
        keypad_frame = tk.Frame(self.root)
        keypad_frame.pack(pady=10, padx=10, fill="both", expand=True)
        
        # Button layout
        buttons = [
            ['7', '8', '9', '/'],
            ['4', '5', '6', '*'],
            ['1', '2', '3', '-'],
            ['0', '.', '=', '+'],
            ['C', 'CE']
        ]
        
        # Create buttons
        for i, row in enumerate(buttons):
            for j, button_text in enumerate(row):
                if button_text == '=':
                    btn = tk.Button(
                        keypad_frame, 
                        text=button_text, 
                        font=('Arial', 15, 'bold'),
                        bg='#4CAF50',
                        fg='white',
                        command=lambda x=button_text: self.on_button_click(x)
                    )
                elif button_text in ['C', 'CE']:
                    btn = tk.Button(
                        keypad_frame, 
                        text=button_text, 
                        font=('Arial', 15, 'bold'),
                        bg='#f44336',
                        fg='white',
                        command=lambda x=button_text: self.on_button_click(x)
                    )
                else:
                    btn = tk.Button(
                        keypad_frame, 
                        text=button_text, 
                        font=('Arial', 15),
                        command=lambda x=button_text: self.on_button_click(x)
                    )
                
                btn.grid(row=i, column=j, sticky="nsew", padx=2, pady=2)
                keypad_frame.grid_columnconfigure(j, weight=1)
            
            keypad_frame.grid_rowconfigure(i, weight=1)
    
    def on_button_click(self, button_text):
        if button_text in '0123456789':
            if self.new_input:
                self.current_input = button_text
                self.new_input = False
            else:
                self.current_input += button_text
            self.update_display()
            
        elif button_text == '.':
            if self.new_input:
                self.current_input = '0.'
                self.new_input = False
            elif '.' not in self.current_input:
                self.current_input += '.'
            self.update_display()
            
        elif button_text in ['+', '-', '*', '/']:
            if self.current_input:
                if self.first_number is None:
                    self.first_number = float(self.current_input)
                else:
                    self.calculate()
                self.operation = button_text
                self.new_input = True
                
        elif button_text == '=':
            if self.first_number is not None and self.operation is not None and not self.new_input:
                self.calculate()
                self.operation = None
                
        elif button_text == 'C':  # Clear all
            self.current_input = ""
            self.first_number = None
            self.operation = None
            self.new_input = True
            self.update_display()
            
        elif button_text == 'CE':  # Clear entry
            self.current_input = ""
            self.new_input = True
            self.update_display()
    
    def calculate(self):
        try:
            second_number = float(self.current_input)
            if self.operation == '+':
                result = self.first_number + second_number
            elif self.operation == '-':
                result = self.first_number - second_number
            elif self.operation == '*':
                result = self.first_number * second_number
            elif self.operation == '/':
                if second_number == 0:
                    messagebox.showerror("Error", "Cannot divide by zero!")
                    self.current_input = ""
                    self.first_number = None
                    self.operation = None
                    self.new_input = True
                    self.update_display()
                    return
                result = self.first_number / second_number
            
            # Format result to avoid unnecessary decimal places
            if result.is_integer():
                result = int(result)
            else:
                result = round(result, 10)
                
            self.current_input = str(result)
            self.first_number = result
            self.new_input = True
            self.update_display()
            
        except ValueError:
            messagebox.showerror("Error", "Invalid input!")
            self.current_input = ""
            self.first_number = None
            self.operation = None
            self.new_input = True
            self.update_display()
    
    def update_display(self):
        self.display.config(state='normal')
        self.display.delete(0, tk.END)
        self.display.insert(0, self.current_input if self.current_input else "0")
        self.display.config(state='readonly')

if __name__ == "__main__":
    root = tk.Tk()
    app = CalculatorApp(root)
    root.mainloop()
