import tkinter as tk
from tkinter import ttk
from math import exp, log, sqrt
from scipy.stats import norm  # For the cumulative distribution function (CDF)

class BlackScholesApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Black-Scholes Option Pricing")
        self.root.geometry("400x400")

        # Create input fields
        self.create_widgets()

    def create_widgets(self):
        # Title
        title_label = tk.Label(self.root, text="Black-Scholes Calculator", font=("Helvetica", 16))
        title_label.pack(pady=10)

        # Input fields
        self.fields = {}
        params = [
            ("Stock Price (S):", "S"),
            ("Strike Price (K):", "K"),
            ("Time to Maturity (T, in years):", "T"),
            ("Risk-Free Rate (r, as decimal):", "r"),
            ("Volatility (σ, as decimal):", "sigma"),
        ]
        
        for label, key in params:
            frame = tk.Frame(self.root)
            frame.pack(pady=5)
            
            tk.Label(frame, text=label).grid(row=0, column=0, padx=5, sticky="w")
            entry = tk.Entry(frame)
            entry.grid(row=0, column=1, padx=5)
            self.fields[key] = entry

        # Option type dropdown
        self.option_type = tk.StringVar(value="call")
        tk.Label(self.root, text="Option Type:").pack(pady=5)
        ttk.Combobox(
            self.root, textvariable=self.option_type, values=["call", "put"]
        ).pack()

        # Calculate button
        calc_button = tk.Button(self.root, text="Calculate", command=self.calculate_option_price)
        calc_button.pack(pady=20)

        # Result label
        self.result_label = tk.Label(self.root, text="", font=("Helvetica", 12), fg="red")
        self.result_label.pack(pady=10)

    def calculate_option_price(self):
        try:
            # Get input values
            S = float(self.fields["S"].get())
            K = float(self.fields["K"].get())
            T = float(self.fields["T"].get())
            r = float(self.fields["r"].get())
            sigma = float(self.fields["sigma"].get())
            option_type = self.option_type.get()

            # Calculate d1 and d2
            d1 = (log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * sqrt(T))
            d2 = d1 - sigma * sqrt(T)

            # Calculate option price
            if option_type == "call":
                price = S * norm.cdf(d1) - K * exp(-r * T) * norm.cdf(d2)
            elif option_type == "put":
                price = K * exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
            else:
                raise ValueError("Invalid option type")

            # Display result
            self.result_label.config(text=f"Option Price: ${price:.2f}")

        except Exception as e:
            self.result_label.config(text=f"Error: {e}", fg="red")

# Main application
if __name__ == "__main__":
    root = tk.Tk()
    app = BlackScholesApp(root)
    root.mainloop()
