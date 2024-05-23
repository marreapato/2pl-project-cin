import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import requests
from io import BytesIO

class TransactionUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Transaction UI")
        self.root.geometry("900x700")  # Increased window size to accommodate new display

        # Define colors
        self.primary_color = "#3498db"
        self.secondary_color = "#2ecc71"
        self.text_color = "#ffffff"
        self.frame_color = "#e74c3c"  # Modern color for the frame

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
        self.selected_protocol.set("Wait-Die")

        self.selected_operations = []

        self.create_widgets()
        self.apply_custom_style()

    def create_widgets(self):
        # Logo
        logo_label = ttk.Label(self.root, image=self.logo)
        logo_label.grid(row=0, column=0, columnspan=3, pady=10)

        # Combo box to select transactions
        transaction_frame = tk.Frame(self.root, bg=self.secondary_color)
        transaction_frame.grid(row=1, column=0, columnspan=3, padx=10, pady=10)
        self.transaction_combo = ttk.Combobox(transaction_frame, textvariable=self.selected_transaction, values=[t["name"] for t in self.transactions], state="readonly")
        self.transaction_combo.pack(pady=10)
        self.transaction_combo.bind("<<ComboboxSelected>>", self.show_transaction_operations)

        # Message display
        message_label = tk.Label(self.root, text="Message Display", bg=self.primary_color, fg=self.text_color)
        message_label.grid(row=2, column=0, columnspan=3, padx=10, pady=(0, 5))
        self.message_display = tk.Text(self.root, height=10, width=80)
        self.message_display.grid(row=3, column=0, columnspan=3, padx=10, pady=(0, 5))

        # Protocol combo box
        protocol_frame = tk.Frame(self.root, bg=self.secondary_color)
        protocol_frame.grid(row=1, column=3, padx=10, pady=10)
        ttk.Label(protocol_frame, text="Protocol").pack(pady=5)
        self.protocol_combo = ttk.Combobox(protocol_frame, textvariable=self.selected_protocol, values=["Wait-Die", "Wound-Wait"], state="readonly")
        self.protocol_combo.pack(pady=5)

        # Buttons
        add_button = ttk.Button(self.root, text="Add Transaction", command=self.add_transaction)
        add_button.grid(row=4, column=0, padx=5, pady=5)
        commit_button = ttk.Button(self.root, text="Commit", command=self.commit_transactions)
        commit_button.grid(row=4, column=1, padx=5, pady=5)
        clear_button = ttk.Button(self.root, text="Clear Display", command=self.clear_display)
        clear_button.grid(row=4, column=2, padx=5, pady=5)

        # Log memory display
        log_memory_label = tk.Label(self.root, text="Log Memory", bg=self.primary_color, fg=self.text_color)
        log_memory_label.grid(row=5, column=0, padx=10, pady=(0, 5))
        self.log_memory = tk.Text(self.root, height=10, width=40)
        self.log_memory.grid(row=6, column=0, padx=10, pady=(0, 5))

        # Log of disk display
        log_disk_label = tk.Label(self.root, text="Log of Disk", bg=self.primary_color, fg=self.text_color)
        log_disk_label.grid(row=5, column=1, padx=10, pady=(0, 5))
        self.log_disk = tk.Text(self.root, height=10, width=40)
        self.log_disk.grid(row=6, column=1, padx=10, pady=(0, 5))

        # Protocol behavior display
        protocol_behavior_label = tk.Label(self.root, text="Protocol Behavior Display", bg=self.primary_color, fg=self.text_color)
        protocol_behavior_label.grid(row=5, column=2, padx=10, pady=(0, 5))
        self.protocol_behavior_display = tk.Text(self.root, height=10, width=40)
        self.protocol_behavior_display.grid(row=6, column=2, padx=10, pady=(0, 5))

    def apply_custom_style(self):
        style = ttk.Style()
        style.theme_create("Modern", parent="alt", settings={
            "TLabel": {"configure": {"background": self.primary_color, "foreground": self.text_color}},
            "TFrame": {"configure": {"background": self.secondary_color}},
            "TCombobox": {"configure": {"background": self.secondary_color, "foreground": self.text_color}},
            "TButton": {"configure": {"background": self.secondary_color, "foreground": self.text_color}},
            "Vertical.TScrollbar": {"configure": {"background": self.primary_color}},
            "TScrollbar": {"configure": {"background": self.primary_color}}
        })
        style.theme_use("Modern")

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
        
        self.message_display.delete(1.0, tk.END)
        self.protocol_behavior_display.delete(1.0, tk.END)

        if deadlock_detected:
            if protocol == "Wait-Die":
                self.message_display.insert(tk.END, "Wait-Die protocol selected\n")
                younger_transaction = self.selected_operations[-1]
                older_transaction = self.selected_operations[-2]
                self.protocol_behavior_display.insert(tk.END, f"{younger_transaction} aborted and rolled back (younger)\n")
                for operation in next(item['operations'] for item in self.transactions if item["name"] == younger_transaction):
                    self.protocol_behavior_display.insert(tk.END, f"Releasing lock on {operation.split()[1]} by {younger_transaction}\n")
                self.protocol_behavior_display.insert(tk.END, f"{older_transaction} continues (older)\n")
                self.selected_operations = [older_transaction]
                self.show_protocol_behavior(older_transaction, wait_die=True)
            elif protocol == "Wound-Wait":
                self.message_display.insert(tk.END, "Wound-Wait protocol selected\n")
                older_transaction = self.selected_operations[0]
                younger_transaction = self.selected_operations[-1]
                self.protocol_behavior_display.insert(tk.END, f"{older_transaction} waits (older)\n")
                self.protocol_behavior_display.insert(tk.END, f"{younger_transaction} continues (younger)\n")
                self.show_protocol_behavior(younger_transaction)
                self.show_protocol_behavior(older_transaction, wait_die=False, continue_after_younger=True)
        else:
            self.log_disk.insert(tk.END, "Committed Transactions:\n")
            for transaction in self.selected_operations:
                self.log_disk.insert(tk.END, f"{transaction}:\n")
                for operation in next(item['operations'] for item in self.transactions if item["name"] == transaction):
                    self.log_disk.insert(tk.END, f" - {operation}\n")
                self.log_disk.insert(tk.END, "\n")

    def show_protocol_behavior(self, transaction, wait_die=False, continue_after_younger=False):
        for operation in next(item['operations'] for item in self.transactions if item["name"] == transaction):
            action, item = operation.split()
            if wait_die and action == "Write":
                self.protocol_behavior_display.insert(tk.END, f"{transaction} writing {item} (lock acquired)\n")
            else:
                self.protocol_behavior_display.insert(tk.END, f"{transaction} {action.lower()}ing {item}\n")
            if continue_after_younger:
                self.protocol_behavior_display.insert(tk.END, f"{transaction} continues after lock on {item} is released\n")
                continue_after_younger = False  # Reset the flag after one use

    def detect_deadlock(self):
        if len(self.selected_operations) < 2:
            return False
        transaction1_ops = next(item['operations'] for item in self.transactions if item["name"] == self.selected_operations[0])
        transaction2_ops = next(item['operations'] for item in self.transactions if item["name"] == self.selected_operations[1])
        for op1 in transaction1_ops:
            action1, item1 = op1.split()
            for op2 in transaction2_ops:
                action2, item2 = op2.split()
                if item1 == item2:
                    return True
        return False

    def clear_display(self):
        self.message_display.delete(1.0, tk.END)
        self.log_memory.delete(1.0, tk.END)
        self.log_disk.delete(1.0, tk.END)
        self.protocol_behavior_display.delete(1.0, tk.END)
        self.selected_operations = []

if __name__ == "__main__":
    root = tk.Tk()
    app = TransactionUI(root)
    root.mainloop()
