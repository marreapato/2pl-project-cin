import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import requests
from io import BytesIO

class TransactionUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Transaction UI")

        # Load logo from web
        logo_url = "https://portal.cin.ufpe.br/wp-content/uploads/2023/06/selo_oficial_6.png"  # Replace with your logo URL
        response = requests.get(logo_url)
        image = Image.open(BytesIO(response.content))

        # Resize the image to a smaller size
        width, height = 100, 100  # Change these values to the desired dimensions
        resized_image = image.resize((width, height))

        self.logo = ImageTk.PhotoImage(resized_image)

        self.transactions = [
            {"name": "Transaction 1", "operations": ["Read x", "Write y"]},
            {"name": "Transaction 2", "operations": ["Read y", "Write x"]},
            {"name": "Transaction 3", "operations": ["Read z", "Write z"]},
            {"name": "Transaction 4", "operations": ["Read x", "Read y", "Write z"]},
            {"name": "Transaction 5", "operations": ["Read y", "Read z", "Write x"]}
        ]

        self.selected_transaction = tk.StringVar()
        self.selected_transaction.set("Select Transaction")

        self.selected_protocol = tk.StringVar()
        self.selected_protocol.set("Normal")

        self.selected_operations = []

        self.create_widgets()

    def create_widgets(self):
        # Logo
        logo_label = ttk.Label(self.root, image=self.logo)
        logo_label.grid(row=0, column=0, columnspan=4, padx=10, pady=10)

        # Combo box to select transactions
        self.transaction_combo = ttk.Combobox(self.root, textvariable=self.selected_transaction, values=[t["name"] for t in self.transactions], state="readonly")
        self.transaction_combo.grid(row=1, column=0, padx=10, pady=10)
        self.transaction_combo.bind("<<ComboboxSelected>>", self.show_transaction_operations)

        # Protocol dropdown menu
        self.protocol_label = tk.Label(self.root, text="Select Protocol:")
        self.protocol_label.grid(row=1, column=1, padx=10, pady=10)
        self.protocol_menu = ttk.Combobox(self.root, textvariable=self.selected_protocol, values=["Normal", "Wait-Die", "Wound-Lock"], state="readonly")
        self.protocol_menu.grid(row=1, column=2, padx=10, pady=10)

        # Button to add transaction
        self.add_button = ttk.Button(self.root, text="Add Transaction", command=self.add_transaction)
        self.add_button.grid(row=1, column=3, padx=10, pady=10)

        # Label for log memory
        self.log_memory_label = tk.Label(self.root, text="Log Memory")
        self.log_memory_label.grid(row=2, column=0, columnspan=4, padx=10, pady=5)

        # Log memory display
        self.log_memory = tk.Text(self.root, height=10, width=60)
        self.log_memory.grid(row=3, column=0, columnspan=4, padx=10, pady=5)

        # Label for log of disk
        self.log_disk_label = tk.Label(self.root, text="Log of Disk")
        self.log_disk_label.grid(row=4, column=0, columnspan=4, padx=10, pady=5)

        # Log of disk display
        self.log_disk = tk.Text(self.root, height=10, width=60)
        self.log_disk.grid(row=5, column=0, columnspan=4, padx=10, pady=5)

        # Label for message display
        self.message_label = tk.Label(self.root, text="Message Display")
        self.message_label.grid(row=6, column=0, columnspan=4, padx=10, pady=5)

        # Message display
        self.message_display = tk.Text(self.root, height=5, width=60)
        self.message_display.grid(row=7, column=0, columnspan=4, padx=10, pady=5)

        # Button to commit transactions
        self.commit_button = ttk.Button(self.root, text="Commit", command=self.commit_transactions)
        self.commit_button.grid(row=8, column=0, columnspan=4, padx=10, pady=10)

    def add_transaction(self):
        selected = self.selected_transaction.get()
        if selected != "Select Transaction":
            if len(self.selected_operations) < 2:
                if selected not in self.selected_operations:
                    self.selected_operations.append(selected)
                    self.update_display()
            else:
                self.message_display.delete(1.0, tk.END)
                self.message_display.insert(tk.END, "Only two transactions can be selected\n")

    def show_transaction_operations(self, event):
        selected = self.selected_transaction.get()
        if selected != "Select Transaction":
            for transaction in self.transactions:
                if transaction["name"] == selected:
                    self.message_display.delete(1.0, tk.END)
                    self.message_display.insert(tk.END, f"{transaction['name']}:\n")
                    for operation in transaction["operations"]:
                        self.message_display.insert(tk.END, f" - {operation}\n")

    def update_display(self):
        self.log_memory.delete(1.0, tk.END)
        for transaction in self.selected_operations:
            self.log_memory.insert(tk.END, f"{transaction}:\n")
            for operation in next(item['operations'] for item in self.transactions if item["name"] == transaction):
                self.log_memory.insert(tk.END, f" - {operation}\n")
            self.log_memory.insert(tk.END, "\n")

    def commit_transactions(self):
        protocol = self.selected_protocol.get()
        deadlock_detected = self.detect_deadlock()

        if deadlock_detected:
            if protocol == "Normal":
                self.message_display.delete(1.0, tk.END)
                self.message_display.insert(tk.END, "Transaction aborted, deadlock occurred\n")
                self.selected_operations = []
                self.log_memory.delete(1.0, tk.END)
            elif protocol == "Wait-Die":
                self.message_display.delete(1.0, tk.END)
                self.message_display.insert(tk.END, "Wait-Die protocol selected\n")
                recent_transaction = self.selected_operations[-1]
                older_transaction = self.selected_operations[-2]
                self.message_display.insert(tk.END, f"{recent_transaction} awaits\n")
                self.message_display.insert(tk.END, f"{older_transaction} finishes\n")
                self.save_to_log_disk()
                self.selected_operations = []
                self.update_display()
            elif protocol == "Wound-Lock":
                self.message_display.delete(1.0, tk.END)
                self.message_display.insert(tk.END, "Wound-Lock protocol selected\n")
                first_transaction = self.selected_operations[0]
                last_transaction = self.selected_operations[-1]
                self.message_display.insert(tk.END, f"{first_transaction} awaits\n")
                self.message_display.insert(tk.END, f"{last_transaction} finishes\n")
                self.save_to_log_disk()
                self.selected_operations = []
                self.update_display()
        else:
            self.log_disk.insert(tk.END, "Committed Transactions:\n")
            for transaction in self.selected_operations:
                self.log_disk.insert(tk.END, f"{transaction}:\n")
                for operation in next(item['operations'] for item in self.transactions if item["name"] == transaction):
                    self.log_disk.insert(tk.END, f" - {operation}\n")
                self.log_disk.insert(tk.END, "\n")
            self.selected_operations = []
            self.update_display()

        if not deadlock_detected:
            self.message_display.delete(1.0, tk.END)
            self.message_display.insert(tk.END, "No deadlock detected, transactions committed normally\n")

    def detect_deadlock(self):
        for transaction1 in self.selected_operations:
            for transaction2 in self.selected_operations:
                if transaction1 != transaction2:
                    operations1 = next(item['operations'] for item in self.transactions if item["name"] == transaction1)
                    operations2 = next(item['operations'] for item in self.transactions if item["name"] == transaction2)
                    for operation1 in operations1:
                        for operation2 in operations2:
                            item1 = operation1.split()[1]
                            item2 = operation2.split()[1]
                            if item1 == item2:
                                return True
        return False

    def save_to_log_disk(self):
        self.log_disk.insert(tk.END, "Committed Transactions:\n")
        for transaction in self.selected_operations:
            self.log_disk.insert(tk.END, f"{transaction}:\n")
            for operation in next(item['operations'] for item in self.transactions if item["name"] == transaction):
                self.log_disk.insert(tk.END, f" - {operation}\n")
            self.log_disk.insert(tk.END, "\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = TransactionUI(root)
    root.mainloop()
