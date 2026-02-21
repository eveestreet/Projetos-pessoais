import json
import tkinter as tk
from tkinter import ttk, messagebox

FILE_PATH = "data/drivers.json"

def smart_number(value):
    num = float(value)
    if num.is_integer():
        return int(num)
    return num


def load_drivers():
    with open(FILE_PATH, "r") as file:
        return json.load(file)


def save_drivers(drivers):
    with open(FILE_PATH, "w") as file:
        json.dump(drivers, file, indent=4)

class DriverApp:

    def __init__(self, root):
        self.root = root
        self.root.title("Championship Manager")
        self.root.geometry("700x450")

        self.drivers = load_drivers()

        self.create_widgets()
        self.populate_table()

    def create_widgets(self):

        columns = ("Name", "Team", "Points", "Podiums", "Wins")
        self.tree = ttk.Treeview(self.root, columns=columns, show="headings")

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120)

        self.tree.pack(pady=10, fill="x")

        frame = tk.Frame(self.root)
        frame.pack(pady=10)

        tk.Label(frame, text="Points:").grid(row=0, column=0)
        self.points_entry = tk.Entry(frame, width=10)
        self.points_entry.grid(row=0, column=1)

        tk.Label(frame, text="Podiums:").grid(row=0, column=2)
        self.podiums_entry = tk.Entry(frame, width=10)
        self.podiums_entry.grid(row=0, column=3)

        tk.Label(frame, text="Wins:").grid(row=0, column=4)
        self.wins_entry = tk.Entry(frame, width=10)
        self.wins_entry.grid(row=0, column=5)

        # Botões
        tk.Button(self.root, text="Edit Selected", command=self.edit_driver).pack(pady=5)
        tk.Button(self.root, text="Add Points", command=self.add_points).pack(pady=5)
        tk.Button(self.root, text="Add Podium", command=self.add_podium).pack(pady=5)
        tk.Button(self.root, text="Add Win", command=self.add_win).pack(pady=5)
        tk.Button(self.root, text="Save", command=self.save).pack(pady=5)

    def populate_table(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        for d in self.drivers:
            self.tree.insert("", "end", values=(
                d["name"],
                d["team"],
                d["points"],
                d["podiums"],
                d["wins"]
            ))

    def get_selected_driver(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Select a driver first!")
            return None

        index = self.tree.index(selected[0])
        return self.drivers[index]

    def edit_driver(self):
        driver = self.get_selected_driver()
        if not driver:
            return

        try:
            if self.points_entry.get():
                driver["points"] = smart_number(self.points_entry.get())

            if self.podiums_entry.get():
                driver["podiums"] = int(self.podiums_entry.get())

            if self.wins_entry.get():
                driver["wins"] = int(self.wins_entry.get())

            self.populate_table()
            messagebox.showinfo("Success", "Driver updated!")

        except ValueError:
            messagebox.showerror("Error", "Invalid number!")

    def add_points(self):
        driver = self.get_selected_driver()
        if not driver:
            return

        try:
            points_to_add = float(self.points_entry.get())
            driver["points"] = smart_number(driver["points"] + points_to_add)

            self.populate_table()
            messagebox.showinfo("Success", "Points added!")

        except ValueError:
            messagebox.showerror("Error", "Enter valid points!")

    # ----------------------

    def add_podium(self):
        driver = self.get_selected_driver()
        if not driver:
            return

        driver["podiums"] += 1
        self.populate_table()
        messagebox.showinfo("Success", "Podium added!")

    # ----------------------

    def add_win(self):
        driver = self.get_selected_driver()
        if not driver:
            return

        driver["wins"] += 1
        driver["podiums"] += 1

        self.populate_table()
        messagebox.showinfo("Success", "Win added!")


    def save(self):
        save_drivers(self.drivers)
        messagebox.showinfo("Saved", "Data saved successfully!")

if __name__ == "__main__":
    root = tk.Tk()
    app = DriverApp(root)
    root.mainloop()
