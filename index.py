import datetime
import sqlite3
from tkcalendar import DateEntry
from tkinter import *
import tkinter.messagebox as mb
import tkinter.ttk as ttk

# Theme Colors
LIGHT_THEME = {
    'primary': '#2c3e50',
    'secondary': '#34495e',
    'accent': '#3498db',
    'bg': '#ecf0f1',
    'text': '#2c3e50',
    'entry_bg': 'white',
    'entry_fg': 'black',
    'button_bg': '#3498db',
    'button_fg': 'white',
    'success': '#2ecc71',
    'warning': '#e74c3c',
    'info': '#3498db'
}

DARK_THEME = {
    'primary': '#212121',
    'secondary': '#424242',
    'accent': '#1976D2',
    'bg': '#121212',
    'text': '#E0E0E0',
    'entry_bg': '#424242',
    'entry_fg': 'white',
    'button_bg': '#1976D2',
    'button_fg': 'white',
    'success': '#388E3C',
    'warning': '#D32F2F',
    'info': '#1976D2'
}

# Global variables
current_theme = LIGHT_THEME
is_fullscreen = False
connector = sqlite3.connect("ExpenseTracker.db")
cursor = connector.cursor()

# Database setup
connector.execute(
    'CREATE TABLE IF NOT EXISTS ExpenseTracker ('
    'ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,'
    'Date DATETIME, Payee TEXT,'
    'Description TEXT, Amount FLOAT,'
    'ModeOfPayment TEXT)'
)
connector.commit()

# Theme functions
def safe_config(widget, **kwargs):
    try:
        widget.config(**kwargs)
    except Exception:
        pass

def apply_theme():
    # Main containers
    safe_config(root, bg=current_theme['bg'])
    safe_config(title_frame, bg=current_theme['primary'])
    safe_config(title_label, bg=current_theme['primary'], fg='white')
    safe_config(data_entry_frame, bg=current_theme['bg'])
    safe_config(buttons_frame, bg=current_theme['bg'])
    safe_config(tree_frame, bg=current_theme['bg'])
    safe_config(status, bg=current_theme['secondary'], fg='white')

    # Data entry widgets
    for widget in data_entry_frame.winfo_children():
        if isinstance(widget, (Label, Button)):
            safe_config(widget, bg=current_theme['bg'], fg=current_theme['text'])
        elif isinstance(widget, (Entry, DateEntry)):
            safe_config(widget, bg=current_theme['entry_bg'], fg=current_theme['entry_fg'])
        elif isinstance(widget, Frame):
            safe_config(widget, bg=current_theme['bg'])
            for child in widget.winfo_children():
                safe_config(child, bg=current_theme['bg'], fg=current_theme['text'])

    # Buttons frame
    for widget in buttons_frame.winfo_children():
        if isinstance(widget, Button):
            safe_config(widget, bg=current_theme['button_bg'], fg=current_theme['button_fg'])

    # Treeview styling
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Treeview",
                  background=current_theme['bg'],
                  foreground=current_theme['text'],
                  fieldbackground=current_theme['bg'])
    style.map('Treeview', background=[('selected', current_theme['accent'])])
    style.configure("Treeview.Heading",
                  background=current_theme['primary'],
                  foreground="white")

def toggle_theme():
    global current_theme
    current_theme = DARK_THEME if current_theme == LIGHT_THEME else LIGHT_THEME
    theme_btn.config(text='☀️ Light Mode' if current_theme == DARK_THEME else '🌙 Dark Mode')
    apply_theme()

# Window controls
def toggle_fullscreen():
    global is_fullscreen
    is_fullscreen = not is_fullscreen
    root.attributes('-fullscreen', is_fullscreen)
    if not is_fullscreen:
        root.geometry('1200x650')

def maximize_window():
    root.state('zoomed')

# Main application
root = Tk()
root.title('Expense Tracker')
root.geometry('1200x650')
root.resizable(True, True)

# Title bar
title_frame = Frame(root, bg=current_theme['primary'])
title_frame.pack(side=TOP, fill=X)

title_label = Label(title_frame, text='EXPENSE TRACKER',
                   font=("Roboto", 14, "bold"),
                   bg=current_theme['primary'], fg="white")
title_label.pack(side=LEFT, padx=10, pady=10)

# Window controls
control_buttons = Frame(title_frame, bg=current_theme['primary'])
control_buttons.pack(side=RIGHT, padx=5)

theme_btn = Button(control_buttons, text='🌙 Dark Mode', font=("Arial", 8),
                  command=toggle_theme, bd=0, highlightthickness=0)
theme_btn.pack(side=LEFT, padx=2)

maximize_btn = Button(control_buttons, text='🗖', font=("Arial", 10),
                     command=maximize_window, bd=0, highlightthickness=0)
maximize_btn.pack(side=LEFT, padx=2)

fullscreen_btn = Button(control_buttons, text='⛶', font=("Arial", 10),
                       command=toggle_fullscreen, bd=0, highlightthickness=0)
fullscreen_btn.pack(side=LEFT, padx=2)

# Main frames
data_entry_frame = Frame(root, bg=current_theme['bg'], bd=2, relief=GROOVE)
data_entry_frame.place(x=20, y=60, width=300, height=580)

buttons_frame = Frame(root, bg=current_theme['bg'], bd=2, relief=GROOVE)
buttons_frame.place(x=340, y=60, width=830, height=100)

tree_frame = Frame(root, bg=current_theme['bg'], bd=2, relief=GROOVE)
tree_frame.place(x=340, y=180, width=830, height=460)

# Data Entry Frame
Label(data_entry_frame, text='ADD NEW EXPENSE',
      font=("Roboto", 14, "bold"),
      bg=current_theme['bg'], fg=current_theme['text']).pack(pady=10)

# Date
date_frame = Frame(data_entry_frame, bg=current_theme['bg'])
date_frame.pack(pady=5, padx=10, fill=X)
Label(date_frame, text='Date:', font=("Open Sans", 12),
      bg=current_theme['bg'], fg=current_theme['text']).pack(side=LEFT)
date = DateEntry(date_frame, date=datetime.datetime.now().date(),
                font=("Open Sans", 11), background=current_theme['primary'],
                foreground='white', borderwidth=2)
date.pack(side=RIGHT, fill=X, expand=True)

# Payee
payee_frame = Frame(data_entry_frame, bg=current_theme['bg'])
payee_frame.pack(pady=5, padx=10, fill=X)
Label(payee_frame, text='Payee:', font=("Open Sans", 12),
      bg=current_theme['bg'], fg=current_theme['text']).pack(side=LEFT)
payee = Entry(payee_frame, font=("Open Sans", 11),
             bg=current_theme['entry_bg'], fg=current_theme['entry_fg'])
payee.pack(side=RIGHT, fill=X, expand=True)

# Description
desc_frame = Frame(data_entry_frame, bg=current_theme['bg'])
desc_frame.pack(pady=5, padx=10, fill=X)
Label(desc_frame, text='Description:', font=("Open Sans", 12),
      bg=current_theme['bg'], fg=current_theme['text']).pack(side=LEFT)
desc = Entry(desc_frame, font=("Open Sans", 11),
            bg=current_theme['entry_bg'], fg=current_theme['entry_fg'])
desc.pack(side=RIGHT, fill=X, expand=True)

# Amount
amount_frame = Frame(data_entry_frame, bg=current_theme['bg'])
amount_frame.pack(pady=5, padx=10, fill=X)
Label(amount_frame, text='Amount:', font=("Open Sans", 12),
      bg=current_theme['bg'], fg=current_theme['text']).pack(side=LEFT)
amount = Entry(amount_frame, font=("Open Sans", 11),
              bg=current_theme['entry_bg'], fg=current_theme['entry_fg'])
amount.pack(side=RIGHT, fill=X, expand=True)

# Payment Mode
payment_frame = Frame(data_entry_frame, bg=current_theme['bg'])
payment_frame.pack(pady=5, padx=10, fill=X)
Label(payment_frame, text='Payment Mode:', font=("Open Sans", 12),
      bg=current_theme['bg'], fg=current_theme['text']).pack(side=LEFT)
payment_mode = StringVar(value='Cash')
payment_dropdown = OptionMenu(payment_frame, payment_mode,
                            'Cash', 'Credit Card', 'Debit Card', 'Online Transfer')
payment_dropdown.config(font=("Open Sans", 11),
                      bg=current_theme['primary'], fg='white')
payment_dropdown.pack(side=RIGHT, fill=X, expand=True)

# Add Expense Button
add_btn = Button(data_entry_frame, text='Add Expense',
                font=("Open Sans", 12, "bold"),
                bg=current_theme['success'], fg='white')
add_btn.pack(pady=20, ipadx=10, ipady=5)

# Buttons Frame
Button(buttons_frame, text='View All', font=("Open Sans", 10, "bold"),
      bg=current_theme['info'], fg='white').place(x=20, y=20)

Button(buttons_frame, text='Edit', font=("Open Sans", 10, "bold"),
      bg=current_theme['accent'], fg='white').place(x=120, y=20)

Button(buttons_frame, text='Delete', font=("Open Sans", 10, "bold"),
      bg=current_theme['warning'], fg='white').place(x=220, y=20)

# Treeview
table = ttk.Treeview(tree_frame, columns=('ID', 'Date', 'Payee', 'Description', 'Amount', 'Payment'))
table.heading('ID', text='ID')
table.heading('Date', text='Date')
table.heading('Payee', text='Payee')
table.heading('Description', text='Description')
table.heading('Amount', text='Amount')
table.heading('Payment', text='Payment')
table.column('#0', width=0, stretch=NO)
table.column('ID', width=50, anchor=CENTER)
table.column('Date', width=100, anchor=CENTER)
table.column('Payee', width=150, anchor=W)
table.column('Description', width=200, anchor=W)
table.column('Amount', width=100, anchor=E)
table.column('Payment', width=150, anchor=W)
table.pack(fill=BOTH, expand=1)

# Status bar
status = Label(root, text="Ready", bd=1, relief=SUNKEN, anchor=W,
              font=("Open Sans", 10), bg=current_theme['secondary'], fg='white')
status.pack(side=BOTTOM, fill=X)

# Apply theme and start
apply_theme()
root.bind('<F11>', lambda e: toggle_fullscreen())
root.mainloop()