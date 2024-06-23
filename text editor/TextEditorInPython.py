import tkinter as tk
from tkinter import filedialog, messagebox

# code for the main window
root = tk.Tk()
root.title("Simple Text Editor")
root.geometry("800x600")

# Create a new Text widget
text_area = tk.Text(root, wrap='word', undo=True)
text_area.pack(expand='yes', fill='both')

# Create a menubar in editor
menu = tk.Menu(root)
root.config(menu=menu)

# Add file menubar
file_menu = tk.Menu(menu, tearoff=0)
menu.add_cascade(label="File", menu=file_menu)

# Add edit menu (undo/redo functionality) .Help to get previous and current edit
edit_menu = tk.Menu(menu, tearoff=0)
menu.add_cascade(label="Edit", menu=edit_menu)

def new_file():
    if text_area.edit_modified():
        if not ask_save_changes():
            return
    text_area.delete(1.0, tk.END)
    root.title("Untitled - Simple Text Editor")

def open_file():
    if text_area.edit_modified():
        if not ask_save_changes():
            return
    file_path = filedialog.askopenfilename(defaultextension=".txt",
                                           filetypes=[("Text Files", "*.txt"),
                                                      ("All Files", "*.*")])
    if not file_path:
        return
    with open(file_path, "r") as file:
        text_area.delete(1.0, tk.END)
        text_area.insert(tk.END, file.read())
    root.title(f"{file_path} - Simple Text Editor")

def save_file():
    file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                             filetypes=[("Text Files", "*.txt"),
                                                        ("All Files", "*.*")])
    if not file_path:
        return
    with open(file_path, "w") as file:
        file.write(text_area.get(1.0, tk.END))
    root.title(f"{file_path} - Simple Text Editor")

def ask_save_changes():
    answer = messagebox.askyesnocancel("Save changes?", "You have unsaved changes. Do you want to save them before continuing?")
    if answer:  # Save changes in editor 
        save_file()
        return True
    elif answer is False:  # Discard changes
        return True
    else:  # Cancel if not required
        return False

file_menu.add_command(label="New", command=new_file)
file_menu.add_command(label="Open", command=open_file)
file_menu.add_command(label="Save", command=save_file)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.quit)

# Optional: Add undo/redo functionality
text_area.bind('<Control-y>', lambda event: text_area.edit_redo())
text_area.bind('<Control-z>', lambda event: text_area.edit_undo())
edit_menu.add_command(label="Undo", command=text_area.edit_undo)
edit_menu.add_command(label="Redo", command=text_area.edit_redo)

# Run the application 
root.mainloop()
