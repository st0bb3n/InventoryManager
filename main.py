import tkinter as tk
from tkinter import ttk
import csv
import sys
from tabulate import tabulate
from PIL import ImageTk, Image

def check_input(input):
    if input == "":
        print("Input is empty")
        return False
    else:
        return True
'''
class ConsoleOutput:
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def write(self, text):
        self.text_widget.insert(tk.END, text)
        self.text_widget.see(tk.END)  # Scroll to the end of the text widget

def clear_text():
    text_output.delete("1.0", tk.END)
'''
def close_last_window():
    if hasattr(show_inventory, 'last_window'):
        show_inventory.last_window.destroy()
        del show_inventory.last_window
    else:
        print("No window to close.")

def remove_linebreaks():
    with open("database.csv", 'r', newline='') as file:
        reader = csv.reader(file)
        rows = list(reader)

    # Remove line breaks within fields
    cleaned_rows = []
    for row in rows:
        cleaned_row = [field.replace('\n', ' ') for field in row]
        cleaned_rows.append(cleaned_row)

    with open("database.csv", 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(cleaned_rows)
'''
def show_inventory():

  #clear_text()
  file_name = "database.csv"
  # Open the CSV file in read mode
  with open(file_name, "r") as file:
      # Create a CSV reader object
      reader = csv.reader(file)

      # Convert the CSV data into a list of rows
      rows = list(reader)

      # Print the table using tabulate
      print(tabulate(rows, headers="firstrow"))
'''

def show_inventory():
    close_last_window()
    file_name = "database.csv"

    # Open the CSV file in read mode
    with open(file_name, "r") as file:
        # Create a CSV reader object
        reader = csv.reader(file)

        # Convert the CSV data into a list of rows
        rows = list(reader)

    # Create a new window for displaying the table
    table_window = tk.Toplevel(window)
    table_window.title("Inventory Table")

    # Create a Treeview widget to display the table as a grid
    treeview = ttk.Treeview(table_window)

    # Define the columns
    columns = rows[0]
    treeview["columns"] = columns

    # Format the columns
    for col in columns:
        treeview.column(col, width=100)
        treeview.heading(col, text=col)

    # Add the data rows
    for row in rows[1:]:
        treeview.insert("", tk.END, values=row)

    # Place the Treeview widget in the grid layout
    treeview.pack()
    
    show_inventory.last_window = table_window

def update_item():
  #clear_text()
  qty, item_code = entry5.get(), entry6.get()
  file_name = "database.csv"

  # Read the existing CSV file and load its contents
  rows = []
  with open(file_name, "r") as file:
      reader = csv.DictReader(file)
      fieldnames = reader.fieldnames
      for row in reader:
          rows.append(row)

  #print(rows)
  # Update the quantity based on the item code

  item_code_exists = False
  for row in rows:
      if row["Item Code"] == item_code:
          row["Quantity"] = str(qty)
          item_code_exists = True
          break

  # Write the updated data back to the CSV file
  if item_code_exists:
      with open(file_name, "w", newline="") as file:
          writer = csv.DictWriter(file, fieldnames=fieldnames)
          writer.writeheader()
          writer.writerows(rows)
      print("CSV file updated successfully.")
  else:
      print("Item code does not exist in the CSV file.")
  show_inventory()

def add_item():
  #clear_text()
  name, qty, item_code, image = entry1.get(), entry2.get(), entry3.get(), entry4.get()
  file_name = "database.csv"

  # Specify the item details to add
  new_item = {
      "Name": name,
      "Quantity": qty,
      "Item Code": item_code,
      "Image": image
  }

  # Read the existing CSV file and load its contents
  rows = []
  with open(file_name, "r") as file:
      reader = csv.DictReader(file)
      fieldnames = reader.fieldnames
      for row in reader:
          rows.append(row)

  # Check if the item code exists and update the quantity
  item_code_exists = False
  for row in rows:
      if row["Item Code"] == new_item["Item Code"]:
          row["Quantity"] = new_item["Quantity"]
          row["Name"] = new_item["Name"]
          item_code_exists = True
          break

  # Add a new row if the item code does not exist
  if not item_code_exists and (check_input(name) and check_input(qty) and check_input(item_code) and check_input(image)):
      rows.append(new_item)

  # Write the updated data back to the CSV file
  with open(file_name, "w", newline="") as file:
      writer = csv.DictWriter(file, fieldnames=fieldnames)
      writer.writeheader()
      writer.writerows(rows)

  print("CSV file updated successfully.")
  show_inventory()

def show_item():
    item_code = entry7.get()
    file_name = "database.csv"

    # Read the CSV file and find the item with the specified item code
    with open(file_name, "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row["Item Code"] == item_code:
                image_path = row["Image"]
                break
        else:
            print("Item code not found in the CSV file.")
            return

    # Load the image using PIL
    try:
        image = Image.open(image_path)
        image = image.resize((300, 300))  # Resize the image as needed
        tk_image = ImageTk.PhotoImage(image)

        # Create a label widget to display the image
        image_label = tk.Label(window, image=tk_image)
        image_label.grid(row=7, column=1, columnspan=2)
        image_label.image = tk_image  # Store a reference to prevent garbage collection

        name_label1 = tk.Label(window, text="Name")
        name_label1.grid(row=4, column=1, columnspan=1)

        name_label2 = tk.Label(window, text="Quantity")
        name_label2.grid(row=5, column=1, columnspan=1)

        name_label3 = tk.Label(window, text="Item Code")
        name_label3.grid(row=6, column=1, columnspan=1)

        name_label4 = tk.Label(window, text=row["Name"])
        name_label4.grid(row=4, column=2, columnspan=1)

        name_label5 = tk.Label(window, text=row["Quantity"])
        name_label5.grid(row=5, column=2, columnspan=1)

        name_label6 = tk.Label(window, text=row["Item Code"])
        name_label6.grid(row=6, column=2, columnspan=1)

    except FileNotFoundError:
        print("Image file not found.")
    

# Create a Tkinter window

window = tk.Tk()
window.title("Personal Inventory Manager")

# Inv and Item
button1 = tk.Button(window, text="Show Inventory", command=show_inventory)
button1.grid(row=0, column=0)

button4 = tk.Button(window, text="Show Item", command=show_item)
button4.grid(row=0, column=1)

entry7 = tk.Entry(window)
entry7.grid(row=0, column=2)
entry7.insert(tk.END, "Item Code")

# Add Item
button2 = tk.Button(window, text="Add Item", command=add_item)
button2.grid(row=1, column=0)

entry1 = tk.Entry(window)
entry1.grid(row=1, column=1)
entry1.insert(tk.END, "Name")

entry2 = tk.Entry(window)
entry2.grid(row=1, column=2)
entry2.insert(tk.END, "Quantity")

entry3 = tk.Entry(window)
entry3.grid(row=2, column=1)
entry3.insert(tk.END, "Item Code")

entry4 = tk.Entry(window)
entry4.grid(row=2, column=2)
entry4.insert(tk.END, "Image Name")

# Create button 3
button3 = tk.Button(window, text="Update Item", command=update_item)
button3.grid(row=3, column=0)

entry5 = tk.Entry(window)
entry5.grid(row=3, column=1)
entry5.insert(tk.END, "Quantity")

entry6 = tk.Entry(window)
entry6.grid(row=3, column=2)
entry6.insert(tk.END, "Item Code")

#text_output = tk.Text(window)
#text_output.grid(row=3, column=0, columnspan=3)

# Redirect console output to the Text widget
#sys.stdout = ConsoleOutput(text_output)

#clear_button = tk.Button(window, text="Clear", command=clear_text)
#clear_button.grid(row=7, column=0)

# Run the Tkinter event loop
window.mainloop()
