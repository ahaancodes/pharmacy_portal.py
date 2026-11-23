import tkinter as tk
from tkinter import messagebox

# 1. Create the main window
window = tk.Tk()
window.title("Simple Hotel Management System")
window.geometry("650x550")
window.configure(bg="#F4F6F9")

# 2. Store rooms and customer bookings in simple Python lists/dictionaries
rooms = {
    "101": {"type": "Single", "price": 1000, "status": "Available"},
    "102": {"type": "Single", "price": 1000, "status": "Available"},
    "201": {"type": "Double", "price": 2000, "status": "Available"},
    "202": {"type": "Double", "price": 2000, "status": "Available"},
    "301": {"type": "Suite", "price": 3500, "status": "Available"},
}

bookings = []  # Stores every customer record


# 3. Function to update the display box on screen
def show_rooms():
  display.delete("1.0", tk.END)
  display.insert(tk.END, "=== HOTEL ROOMS ===\n\n")
  for room_no, info in rooms.items():
    line = (
        f"Room {room_no}  |  {info['type']}  |  ₹{info['price']}/night  | "
        f" {info['status']}\n"
    )
    display.insert(tk.END, line)


# 4. Function to Book a Room (Check-In)
def book_room():
  name = name_entry.get().strip()
  phone = phone_entry.get().strip()
  room_no = room_entry.get().strip()
  days_text = days_entry.get().strip()

  if not name or not phone or not room_no or not days_text:
    messagebox.showwarning("Missing Info", "Please fill all 4 boxes!")
    return

  if room_no not in rooms:
    messagebox.showerror("Error", "Room number does not exist! Use 101-301.")
    return

  if rooms[room_no]["status"] != "Available":
    messagebox.showerror("Error", f"Room {room_no} is already occupied!")
    return

  try:
    days = int(days_text)
    if days <= 0:
      raise ValueError
  except ValueError:
    messagebox.showerror("Error", "Days must be a valid number (1 or more).")
    return

  # Calculate total bill
  price = rooms[room_no]["price"]
  total_bill = price * days

  # Mark room as Occupied and save customer record
  rooms[room_no]["status"] = "Occupied"
  bookings.append({
      "name": name,
      "phone": phone,
      "room": room_no,
      "days": days,
      "bill": total_bill,
      "status": "Checked-In",
  })

  # Clear input boxes
  name_entry.delete(0, tk.END)
  phone_entry.delete(0, tk.END)
  room_entry.delete(0, tk.END)
  days_entry.delete(0, tk.END)

  show_rooms()
  messagebox.showinfo(
      "Booked!", f"Room {room_no} booked for {name}!\nTotal Bill: ₹{total_bill}"
  )


# 5. Function to Check-Out & Print Bill
def checkout_room():
  room_no = room_entry.get().strip()

  if room_no not in rooms or rooms[room_no]["status"] == "Available":
    messagebox.showerror(
        "Error", "Enter an Occupied Room Number in the Room box to check out."
    )
    return

  # Find the active booking for this room
  for record in bookings:
    if record["room"] == room_no and record["status"] == "Checked-In":
      record["status"] = "Checked-Out"
      rooms[room_no]["status"] = "Available"

      # Show bill in the display box
      display.delete("1.0", tk.END)
      display.insert(tk.END, "=== FINAL CUSTOMER BILL ===\n\n")
      display.insert(tk.END, f"Customer Name : {record['name']}\n")
      display.insert(tk.END, f"Phone Number  : {record['phone']}\n")
      display.insert(tk.END, f"Room Number   : {record['room']}\n")
      display.insert(tk.END, f"Days Stayed   : {record['days']}\n")
      display.insert(tk.END, f"Total Paid    : ₹{record['bill']}\n")
      display.insert(tk.END, "\nRoom is now Available again!")

      room_entry.delete(0, tk.END)
      messagebox.showinfo(
          "Checked Out", f"{record['name']} checked out! Bill: ₹{record['bill']}"
      )
      return


# 6. Function to View All Customer Records
def show_records():
  display.delete("1.0", tk.END)
  display.insert(tk.END, "=== CUSTOMER RECORDS ===\n\n")
  if not bookings:
    display.insert(tk.END, "No bookings yet.\n")
    return

  for b in bookings:
    line = (
        f"{b['name']} ({b['phone']})  |  Room {b['room']}  |  {b['days']}"
        f" days  |  ₹{b['bill']}  |  {b['status']}\n"
    )
    display.insert(tk.END, line)


# ---------------- SCREEN LAYOUT (LABELS, INPUTS & BUTTONS) ----------------
tk.Label(
    window,
    text="🏨 Hotel Management System",
    font=("Arial", 18, "bold"),
    bg="#F4F6F9",
    fg="#1E3A8A",
).pack(pady=10)

form_frame = tk.Frame(window, bg="#F4F6F9")
form_frame.pack(pady=5)

tk.Label(form_frame, text="Customer Name:", font=("Arial", 11), bg="#F4F6F9").grid(
    row=0, column=0, sticky="e", padx=5, pady=5
)
name_entry = tk.Entry(form_frame, font=("Arial", 11), width=25)
name_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(form_frame, text="Phone Number:", font=("Arial", 11), bg="#F4F6F9").grid(
    row=1, column=0, sticky="e", padx=5, pady=5
)
phone_entry = tk.Entry(form_frame, font=("Arial", 11), width=25)
phone_entry.grid(row=1, column=1, padx=5, pady=5)

tk.Label(
    form_frame, text="Room No (101-301):", font=("Arial", 11), bg="#F4F6F9"
).grid(row=2, column=0, sticky="e", padx=5, pady=5)
room_entry = tk.Entry(form_frame, font=("Arial", 11), width=25)
room_entry.grid(row=2, column=1, padx=5, pady=5)

tk.Label(form_frame, text="Number of Days:", font=("Arial", 11), bg="#F4F6F9").grid(
    row=3, column=0, sticky="e", padx=5, pady=5
)
days_entry = tk.Entry(form_frame, font=("Arial", 11), width=25)
days_entry.grid(row=3, column=1, padx=5, pady=5)

# Buttons Row
btn_frame = tk.Frame(window, bg="#F4F6F9")
btn_frame.pack(pady=12)

tk.Button(
    btn_frame,
    text="Book Room (Check-In)",
    font=("Arial", 10, "bold"),
    bg="#16A34A",
    fg="white",
    padx=10,
    pady=6,
    command=book_room,
).grid(row=0, column=0, padx=5)
tk.Button(
    btn_frame,
    text="Check-Out & Bill",
    font=("Arial", 10, "bold"),
    bg="#DC2626",
    fg="white",
    padx=10,
    pady=6,
    command=checkout_room,
).grid(row=0, column=1, padx=5)
tk.Button(
    btn_frame,
    text="Show Rooms",
    font=("Arial", 10, "bold"),
    bg="#2563EB",
    fg="white",
    padx=10,
    pady=6,
    command=show_rooms,
).grid(row=0, column=2, padx=5)
tk.Button(
    btn_frame,
    text="Customer Records",
    font=("Arial", 10, "bold"),
    bg="#4B5563",
    fg="white",
    padx=10,
    pady=6,
    command=show_records,
).grid(row=0, column=3, padx=5)

# Output Screen Box
display = tk.Text(window, height=14, width=72, font=("Consolas", 10))
display.pack(pady=10)

# Show rooms right when the app opens
show_rooms()

# Start the app
window.mainloop()