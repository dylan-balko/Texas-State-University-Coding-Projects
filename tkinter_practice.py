import tkinter as tk

class BusinessAppGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Business Management Application")

        # Setup the UI
        self.setup_ui()

    def setup_ui(self):
        # Buttons to select functionality
        self.name_button = tk.Button(self.root, text="Enter Name", command=self.show_name_input)
        self.name_button.pack()

        self.discount_button = tk.Button(self.root, text="Calculate Discount", command=self.show_discount_calculator)
        self.discount_button.pack()

        # Frame to hold the widgets for each feature
        self.feature_frame = tk.Frame(self.root)
        self.feature_frame.pack()

    def show_name_input(self):
        # Clear the frame and add name input widgets
        self.clear_frame()
        tk.Label(self.feature_frame, text="Enter your name:").pack()
        self.name_entry = tk.Entry(self.feature_frame)
        self.name_entry.pack()
        tk.Button(self.feature_frame, text="Submit", command=self.display_name).pack()
        self.result_label = tk.Label(self.feature_frame, text="")
        self.result_label.pack()

    def show_discount_calculator(self):
        # Clear the frame and add discount calculator widgets
        self.clear_frame()
        tk.Label(self.feature_frame, text="Enter the product price:").pack()
        self.price_entry = tk.Entry(self.feature_frame)
        self.price_entry.pack()

        tk.Label(self.feature_frame, text="Enter the discount (%):").pack()
        self.discount_entry = tk.Entry(self.feature_frame)
        self.discount_entry.pack()

        tk.Button(self.feature_frame, text="Calculate", command=self.calculate_discount).pack()
        self.result_label = tk.Label(self.feature_frame, text="")
        self.result_label.pack()

    def clear_frame(self):
        for widget in self.feature_frame.winfo_children():
            widget.destroy()

    def display_name(self):
        name = self.name_entry.get()
        self.result_label.config(text=f"Welcome, {name}!")

    def calculate_discount(self):
        try:
            price = float(self.price_entry.get())
            discount = float(self.discount_entry.get())
            discounted_price = price - (price * discount / 100)
            self.result_label.config(text=f"Discounted Price: ${discounted_price:.2f}")
        except ValueError:
            self.result_label.config(text="Please enter valid numbers.")

def create_app():
    root = tk.Tk()
    app = BusinessAppGUI(root)
    return app

app = create_app()
app.root.mainloop()
