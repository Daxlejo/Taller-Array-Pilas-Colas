import tkinter as tk
from tkinter import ttk
import random


class Order():
    def __init__(self,id,destination,category):
        self.id = id
        self.destination = destination
        self.category = category

    def __str__(self):
        return f"Order {self.id} -> {self.destination} ({self.category})"

class  QueueOrders():
    def __init__(self):
        self.queue = []
        self.next = 1

    def in_queue(self, destination, category):
        order = Order(self.next, destination, category)
        self.queue.append(order)
        self.next += 1

    def de_queue(self):
        if not self.is_empty():
            self.queue.pop(0)
        return None

    def is_empty(self):
        return not self.queue
    

class Godown():
    def __init__(self):
        self.storage = {}

    def add_order(self, order):
        category = order.category
        if category not in self.storage:
            self.storage[category] = []
        self.storage[category].append(order)
    
    def orders_by_category(self, category):
        return self.storage.get(category, [])
    
    def is_empty(self):
        return not self.storage
    

class DeliveryTruck():
    def __init__(self):
        self.load = []

    def load_truck(self, order):
        self.load.append(order)

    def unload_truck(self):
        if not self.load:
            return "The truck is Empty"
        order = self.load.pop()
        return f"Order {order.id} was delivered in {order.destination} - {order.category}"


class App:

    def __init__(self):
        self.queue = QueueOrders()
        self.godown = Godown()
        self.truck = DeliveryTruck()

        self.root = tk.Tk()
        self.root.title("AmazonHUB")
        self.root.geometry("900x520")
        self.root.resizable(False, False)
        self.root.configure(bg="#0b1120")

        self.build_ui()
        self.root.mainloop()

    def build_ui(self):

        header = tk.Frame(self.root, bg="#0f172a", height=60)
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(
            header,
            text="AmazonHUB",
            bg="#0f172a",
            fg="white",
            font=("Segoe UI", 18, "bold")
        ).pack(side="left", padx=25)

        tk.Label(
            header,
            text="Logistics Control Panel",
            bg="#0f172a",
            fg="#94a3b8",
            font=("Segoe UI", 10)
        ).pack(side="left")

        controls = tk.Frame(self.root, bg="#020617", height=70)
        controls.pack(fill="x")
        controls.pack_propagate(False)

        btn_style = {
            "bg": "#2563eb",
            "fg": "white",
            "activebackground": "#3b82f6",
            "activeforeground": "white",
            "relief": "flat",
            "font": ("Segoe UI", 11, "bold"),
            "width": 16,
            "padx": 5,
            "pady": 6
        }

        tk.Button(controls, text="➕ New Order", command=self.add_order, **btn_style).pack(side="left", padx=25)
        tk.Button(controls, text="📦 Load Truck", command=self.load_truck, **btn_style).pack(side="left", padx=15)
        tk.Button(controls, text="🚚 Deliver Order", command=self.deliver_order, **btn_style).pack(side="left", padx=15)

        main = tk.Frame(self.root, bg="#0b1120")
        main.pack(fill="both", expand=True)

        self.log_box = tk.Text(
            main,
            bg="#020617",
            fg="#e5e7eb",
            font=("Consolas", 11),
            relief="flat",
            padx=15,
            pady=15,
            width=40,
            height=20
        )
        self.log_box.pack(side="left", fill="both", expand=False, padx=(25,10), pady=20)
        self.log_box.insert("end", "System ready...\nWaiting for orders...\n")
        self.log_box.tag_configure("delivered", foreground="red")
        self.log_box.tag_configure("new_order", foreground="#facc15")
        self.log_box.tag_configure("loaded_truck", foreground="#22c55e")

        right_panel = tk.Frame(main, bg="#0b1120")
        right_panel.pack(side="left", fill="both", expand=True, padx=(10,25), pady=20)

        tk.Label(right_panel, text="Orders Queue", bg="#0b1120", fg="#facc15", font=("Segoe UI", 12, "bold")).pack()
        self.queue_list = tk.Listbox(right_panel, bg="#1e293b", fg="white", font=("Segoe UI", 11))
        self.queue_list.pack(fill="both", expand=True, pady=5)

        tk.Label(right_panel, text="Truck Load", bg="#0b1120", fg="#22c55e", font=("Segoe UI", 12, "bold")).pack(pady=(10,0))
        self.truck_list = tk.Listbox(right_panel, bg="#1e293b", fg="white", font=("Segoe UI", 11), height=10)
        self.truck_list.pack(fill="both", expand=True, pady=5)

        tk.Label(right_panel, text="Godown", bg="#0b1120", fg="#f472b6", font=("Segoe UI", 12, "bold")).pack(pady=(10,0))
        self.godown_list = tk.Listbox(right_panel, bg="#1e293b", fg="white", font=("Segoe UI", 11))
        self.godown_list.pack(fill="both", expand=True, pady=5)


    def add_order(self):
        destinations = ["Bogotá", "Cali", "Medellín", "Barranquilla", "Pasto", "Popayan"]
        categories = ["Electronics", "Books", "Clothes", "Toys", "Accessories"]

        destination = random.choice(destinations)
        category = random.choice(categories)

        self.queue.in_queue(destination, category)
        order = self.queue.queue[-1]
        self.godown.add_order(order)

        self.log_box.insert("end", f"New order added: {order}\n", "new_order")
        self.log_box.see("end")
        self.update_lists()

    def load_truck(self):
        if self.queue.is_empty():
            self.log_box.insert("end", "No orders in queue to load.\n")
            self.log_box.see("end")
            return

        order = self.queue.queue[0]
        self.truck.load_truck(order)
        self.queue.de_queue()

        self.log_box.insert("end", f"Order loaded onto truck: {order}\n", "loaded_truck")
        self.log_box.see("end")
        self.update_lists()

    def deliver_order(self):
        result = self.truck.unload_truck()
        self.log_box.insert("end", f"{result}\n", "delivered")
        self.log_box.see("end")
        self.update_lists()

    def update_lists(self):
        self.queue_list.delete(0, "end")
        for order in self.queue.queue:
            self.queue_list.insert("end", str(order))

        self.truck_list.delete(0, "end")
        for order in self.truck.load:
            self.truck_list.insert("end", str(order))

        self.godown_list.delete(0, "end")
        for category, orders in self.godown.storage.items():
            for order in orders:
                self.godown_list.insert("end", f"{order}")
                

app = App()