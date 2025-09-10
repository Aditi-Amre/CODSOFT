import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import json
import os
from datetime import datetime

class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("TaskMaster - Your Personal To-Do List")
        self.root.geometry("800x600")
        self.root.configure(bg='#f5f5f5')
        self.root.resizable(True, True)
        
        # Initialize tasks list
        self.tasks = []
        
        # Load previous tasks if available
        self.load_tasks()
        
        # Setup the UI
        self.setup_ui()
        
        # Populate tasks
        self.update_task_list()
    
    def setup_ui(self):
        # Header frame
        header_frame = tk.Frame(self.root, bg='#4CAF50', height=80)
        header_frame.pack(fill='x', padx=10, pady=10)
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(header_frame, text="TaskMaster", font=('Arial', 24, 'bold'), 
                              fg='white', bg='#4CAF50')
        title_label.pack(side='left', padx=20)
        
        date_label = tk.Label(header_frame, text=datetime.now().strftime("%A, %B %d, %Y"), 
                             font=('Arial', 12), fg='white', bg='#4CAF50')
        date_label.pack(side='right', padx=20)
        
        # Input frame
        input_frame = tk.Frame(self.root, bg='#f5f5f5')
        input_frame.pack(fill='x', padx=20, pady=10)
        
        self.task_entry = tk.Entry(input_frame, font=('Arial', 14), width=40)
        self.task_entry.pack(side='left', padx=(0, 10), fill='x', expand=True)
        self.task_entry.bind('<Return>', lambda e: self.add_task())
        
        add_button = tk.Button(input_frame, text="Add Task", command=self.add_task, 
                              bg='#4CAF50', fg='white', font=('Arial', 12, 'bold'),
                              relief='flat', padx=15)
        add_button.pack(side='right')
        
        # Filter frame
        filter_frame = tk.Frame(self.root, bg='#f5f5f5')
        filter_frame.pack(fill='x', padx=20, pady=(0, 10))
        
        tk.Label(filter_frame, text="Filter:", font=('Arial', 10), bg='#f5f5f5').pack(side='left')
        
        self.filter_var = tk.StringVar(value="All")
        filter_combo = ttk.Combobox(filter_frame, textvariable=self.filter_var, 
                                   values=["All", "Completed", "Pending"], width=12, state="readonly")
        filter_combo.pack(side='left', padx=10)
        filter_combo.bind('<<ComboboxSelected>>', lambda e: self.update_task_list())
        
        # Tasks frame
        tasks_frame = tk.Frame(self.root, bg='#f5f5f5')
        tasks_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Create a treeview with scrollbar
        tree_frame = tk.Frame(tasks_frame)
        tree_frame.pack(fill='both', expand=True)
        
        columns = ('status', 'task', 'date')
        self.tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=15)
        
        # Define headings
        self.tree.heading('status', text='Status', command=lambda: self.sort_by_column('status', False))
        self.tree.heading('task', text='Task', command=lambda: self.sort_by_column('task', False))
        self.tree.heading('date', text='Date Added', command=lambda: self.sort_by_column('date', False))
        
        # Define columns
        self.tree.column('status', width=100, anchor='center')
        self.tree.column('task', width=400, anchor='w')
        self.tree.column('date', width=150, anchor='center')
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Bind double click to edit task
        self.tree.bind('<Double-1>', self.edit_task)
        
        # Buttons frame
        buttons_frame = tk.Frame(self.root, bg='#f5f5f5')
        buttons_frame.pack(fill='x', padx=20, pady=10)
        
        complete_button = tk.Button(buttons_frame, text="Mark Complete", command=self.mark_complete,
                                   bg='#2196F3', fg='white', font=('Arial', 10))
        complete_button.pack(side='left', padx=5)
        
        edit_button = tk.Button(buttons_frame, text="Edit Task", command=self.edit_task,
                               bg='#FF9800', fg='white', font=('Arial', 10))
        edit_button.pack(side='left', padx=5)
        
        delete_button = tk.Button(buttons_frame, text="Delete Task", command=self.delete_task,
                                 bg='#F44336', fg='white', font=('Arial', 10))
        delete_button.pack(side='left', padx=5)
        
        clear_button = tk.Button(buttons_frame, text="Clear Completed", command=self.clear_completed,
                                bg='#9E9E9E', fg='white', font=('Arial', 10))
        clear_button.pack(side='right', padx=5)
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set(f"Total Tasks: {len(self.tasks)} | Completed: {len([t for t in self.tasks if t['completed']])}")
        
        status_bar = tk.Label(self.root, textvariable=self.status_var, bd=1, relief=tk.SUNKEN, 
                             anchor=tk.W, bg='#E0E0E0', font=('Arial', 10))
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def add_task(self):
        task_text = self.task_entry.get().strip()
        if task_text:
            task = {
                'id': len(self.tasks) + 1,
                'text': task_text,
                'completed': False,
                'date_added': datetime.now().strftime("%Y-%m-%d %H:%M")
            }
            self.tasks.append(task)
            self.task_entry.delete(0, tk.END)
            self.update_task_list()
            self.save_tasks()
        else:
            messagebox.showwarning("Warning", "Please enter a task!")
    
    def update_task_list(self):
        # Clear the treeview
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Filter tasks
        filter_value = self.filter_var.get()
        if filter_value == "Completed":
            display_tasks = [t for t in self.tasks if t['completed']]
        elif filter_value == "Pending":
            display_tasks = [t for t in self.tasks if not t['completed']]
        else:
            display_tasks = self.tasks
        
        # Add tasks to treeview
        for task in display_tasks:
            status = "✓" if task['completed'] else "○"
            self.tree.insert('', tk.END, values=(status, task['text'], task['date_added']), iid=task['id'])
        
        # Update status bar
        total_tasks = len(self.tasks)
        completed_tasks = len([t for t in self.tasks if t['completed']])
        self.status_var.set(f"Total Tasks: {total_tasks} | Completed: {completed_tasks} | Pending: {total_tasks - completed_tasks}")
    
    def mark_complete(self):
        selected = self.tree.selection()
        if selected:
            task_id = int(selected[0])
            for task in self.tasks:
                if task['id'] == task_id:
                    task['completed'] = not task['completed']
                    break
            self.update_task_list()
            self.save_tasks()
        else:
            messagebox.showwarning("Warning", "Please select a task to mark as complete!")
    
    def edit_task(self, event=None):
        selected = self.tree.selection()
        if selected:
            task_id = int(selected[0])
            for task in self.tasks:
                if task['id'] == task_id:
                    new_text = simpledialog.askstring("Edit Task", "Modify your task:", initialvalue=task['text'])
                    if new_text and new_text.strip():
                        task['text'] = new_text.strip()
                        self.update_task_list()
                        self.save_tasks()
                    break
        else:
            messagebox.showwarning("Warning", "Please select a task to edit!")
    
    def delete_task(self):
        selected = self.tree.selection()
        if selected:
            if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this task?"):
                task_id = int(selected[0])
                self.tasks = [t for t in self.tasks if t['id'] != task_id]
                self.update_task_list()
                self.save_tasks()
        else:
            messagebox.showwarning("Warning", "Please select a task to delete!")
    
    def clear_completed(self):
        if any(task['completed'] for task in self.tasks):
            if messagebox.askyesno("Confirm Clear", "Are you sure you want to clear all completed tasks?"):
                self.tasks = [t for t in self.tasks if not t['completed']]
                self.update_task_list()
                self.save_tasks()
        else:
            messagebox.showinfo("Info", "There are no completed tasks to clear!")
    
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
    
    def save_tasks(self):
        with open('tasks.json', 'w') as f:
            json.dump(self.tasks, f)
    
    def load_tasks(self):
        if os.path.exists('tasks.json'):
            try:
                with open('tasks.json', 'r') as f:
                    self.tasks = json.load(f)
            except:
                self.tasks = []
        else:
            self.tasks = []

def main():
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()