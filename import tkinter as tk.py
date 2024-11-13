import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import sqlite3
import re

# Create or connect to SQLite database
conn = sqlite3.connect('family_data.db')
cursor = conn.cursor()

# Ensure the table has all necessary columns
try:
    cursor.execute("ALTER TABLE family ADD COLUMN phone TEXT")
except sqlite3.OperationalError:
    pass  # Column already exists

try:
    cursor.execute("ALTER TABLE family ADD COLUMN email TEXT")
except sqlite3.OperationalError:
    pass  # Column already exists

try:
    cursor.execute("ALTER TABLE family ADD COLUMN address TEXT")
except sqlite3.OperationalError:
    pass  # Column already exists

# Commit changes
conn.commit()

# Create table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS family (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        age INTEGER NOT NULL,
        relationship TEXT NOT NULL,
        phone TEXT,
        email TEXT,
        address TEXT
    )
''')
conn.commit()

# Function to insert family data into the database
def insert_data():
    name = name_entry.get()
    age = age_entry.get()
    relationship = relationship_entry.get()
    phone = phone_entry.get()
    email = email_entry.get()
    address = address_entry.get()

    # Validate inputs
    if not name or not age or not relationship:
        messagebox.showerror("Input Error", "Name, Age, and Relationship are required fields!")
        return

    if not age.isdigit() or int(age) <= 0:
        messagebox.showerror("Input Error", "Age must be a valid positive number!")
        return

    if phone and not validate_phone(phone):
        messagebox.showerror("Input Error", "Phone number is not valid!")
        return

    if email and not validate_email(email):
        messagebox.showerror("Input Error", "Email address is not valid!")
        return

    try:
        age = int(age)  # Ensure age is an integer
        cursor.execute('''
            INSERT INTO family (name, age, relationship, phone, email, address)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (name, age, relationship, phone, email, address))
        conn.commit()
        messagebox.showinfo("Success", "Family data saved successfully!")
        clear_fields()
    except Exception as e:
        messagebox.showerror("Database Error", f"An error occurred: {e}")

# Function to clear input fields after saving
def clear_fields():
    name_entry.delete(0, tk.END)
    age_entry.delete(0, tk.END)
    relationship_entry.delete(0, tk.END)
    phone_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)
    address_entry.delete(0, tk.END)

# Function to validate phone number (basic validation)
def validate_phone(phone):
    return bool(re.match(r'^\+?\d{10,15}$', phone))

# Function to validate email address
def validate_email(email):
    return bool(re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email))

# Function to show all family data with sorting options
def show_family_data():
    cursor.execute("SELECT * FROM family")
    rows = cursor.fetchall()

    # Create a new window to show data
    display_window = tk.Toplevel(root)
    display_window.title("Family Members List")

    # Scrollable frame for family data display
    canvas = tk.Canvas(display_window)
    scrollbar = tk.Scrollbar(display_window, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)

    scrollable_frame = tk.Frame(canvas)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    scrollbar.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)

    # Display family data with a creative layout
    for row in rows:
        member_info = f"ID: {row[0]} | Name: {row[1]} | Age: {row[2]} | Relationship: {row[3]} | Phone: {row[4]} | Email: {row[5]} | Address: {row[6]}"
        label = tk.Label(scrollable_frame, text=member_info, anchor="w", font=("Helvetica", 10), bg="#f0f0f0", padx=10, pady=5)
        label.pack(fill="x", padx=10, pady=2)

# Function to update family data
def update_family_data():
    try:
        selected_id = int(family_id_entry.get())
        name = name_entry.get()
        age = age_entry.get()
        relationship = relationship_entry.get()
        phone = phone_entry.get()
        email = email_entry.get()
        address = address_entry.get()

        if not name or not age or not relationship:
            messagebox.showerror("Input Error", "Name, Age, and Relationship are required fields!")
            return

        if not age.isdigit() or int(age) <= 0:
            messagebox.showerror("Input Error", "Age must be a valid positive number!")
            return

        if phone and not validate_phone(phone):
            messagebox.showerror("Input Error", "Phone number is not valid!")
            return

        if email and not validate_email(email):
            messagebox.showerror("Input Error", "Email address is not valid!")
            return

        cursor.execute('''
            UPDATE family
            SET name = ?, age = ?, relationship = ?, phone = ?, email = ?, address = ?
            WHERE id = ?
        ''', (name, int(age), relationship, phone, email, address, selected_id))
        conn.commit()

        messagebox.showinfo("Success", "Family data updated successfully!")
        clear_fields()
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

# Function to delete a family member with confirmation
def delete_family_member():
    try:
        selected_id = int(family_id_entry.get())
        confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this family member?")
        if confirm:
            cursor.execute('DELETE FROM family WHERE id = ?', (selected_id,))
            conn.commit()
            messagebox.showinfo("Success", "Family member deleted successfully!")
            clear_fields()
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

# Function to search family members by name or relationship
def search_family_data():
    search_term = search_entry.get().lower()
    cursor.execute("SELECT * FROM family WHERE name LIKE ? OR relationship LIKE ?", ('%' + search_term + '%', '%' + search_term + '%'))
    rows = cursor.fetchall()

    # Display search results in a new window
    search_window = tk.Toplevel(root)
    search_window.title(f"Search Results for '{search_term}'")

    if not rows:
        tk.Label(search_window, text="No results found.", font=("Helvetica", 12), fg="red").pack(padx=10, pady=10)
    else:
        canvas = tk.Canvas(search_window)
        scrollbar = tk.Scrollbar(search_window, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)

        scrollable_frame = tk.Frame(canvas)
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        # Display search results
        for row in rows:
            member_info = f"ID: {row[0]} | Name: {row[1]} | Age: {row[2]} | Relationship: {row[3]} | Phone: {row[4]} | Email: {row[5]} | Address: {row[6]}"
            label = tk.Label(scrollable_frame, text=member_info, anchor="w", font=("Helvetica", 10), bg="#e0e0e0", padx=10, pady=5)
            label.pack(fill="x", padx=10, pady=2)

# Create main window
root = tk.Tk()
root.title("Family Data Entry")

# Styling
root.configure(bg="#f4f4f9")
root.geometry("600x600")

# Create labels and entry fields
tk.Label(root, text="Family Member ID (for Update/Delete):", bg="#f4f4f9", font=("Helvetica", 10)).grid(row=0, column=0, padx=10, pady=10)
family_id_entry = tk.Entry(root, font=("Helvetica", 12))
family_id_entry.grid(row=0, column=1)

tk.Label(root, text="Name:", bg="#f4f4f9", font=("Helvetica", 10)).grid(row=1, column=0, padx=10, pady=10)
name_entry = tk.Entry(root, font=("Helvetica", 12))
name_entry.grid(row=1, column=1)

tk.Label(root, text="Age:", bg="#f4f4f9", font=("Helvetica", 10)).grid(row=2, column=0, padx=10, pady=10)
age_entry = tk.Entry(root, font=("Helvetica", 12))
age_entry.grid(row=2, column=1)

tk.Label(root, text="Relationship:", bg="#f4f4f9", font=("Helvetica", 10)).grid(row=3, column=0, padx=10, pady=10)
relationship_entry = tk.Entry(root, font=("Helvetica", 12))
relationship_entry.grid(row=3, column=1)

tk.Label(root, text="Phone:", bg="#f4f4f9", font=("Helvetica", 10)).grid(row=4, column=0, padx=10, pady=10)
phone_entry = tk.Entry(root, font=("Helvetica", 12))
phone_entry.grid(row=4, column=1)

tk.Label(root, text="Email:", bg="#f4f4f9", font=("Helvetica", 10)).grid(row=5, column=0, padx=10, pady=10)
email_entry = tk.Entry(root, font=("Helvetica", 12))
email_entry.grid(row=5, column=1)

tk.Label(root, text="Address:", bg="#f4f4f9", font=("Helvetica", 10)).grid(row=6, column=0, padx=10, pady=10)
address_entry = tk.Entry(root, font=("Helvetica", 12))
address_entry.grid(row=6, column=1)

# Create buttons
submit_button = tk.Button(root, text="Submit", command=insert_data, bg="#4CAF50", fg="white", font=("Helvetica", 12))
submit_button.grid(row=7, column=0, columnspan=2, pady=10)

update_button = tk.Button(root, text="Update", command=update_family_data, bg="#FFA500", fg="white", font=("Helvetica", 12))
update_button.grid(row=8, column=0, columnspan=2, pady=10)

delete_button = tk.Button(root, text="Delete", command=delete_family_member, bg="#FF6347", fg="white", font=("Helvetica", 12))
delete_button.grid(row=9, column=0, columnspan=2, pady=10)

show_button = tk.Button(root, text="Show All Family Members", command=show_family_data, bg="#1E90FF", fg="white", font=("Helvetica", 12))
show_button.grid(row=10, column=0, columnspan=2, pady=10)

search_label = tk.Label(root, text="Search by Name/Relationship:", bg="#f4f4f9", font=("Helvetica", 10))
search_label.grid(row=11, column=0, padx=10, pady=10)
search_entry = tk.Entry(root, font=("Helvetica", 12))
search_entry.grid(row=11, column=1)

search_button = tk.Button(root, text="Search", command=search_family_data, bg="#32CD32", fg="white", font=("Helvetica", 12))
search_button.grid(row=12, column=0, columnspan=2, pady=10)

# Run the application
root.mainloop()

# Close the database connection on exit
conn.close()
