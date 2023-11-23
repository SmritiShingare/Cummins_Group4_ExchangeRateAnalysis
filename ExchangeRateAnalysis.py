import pandas as pd
import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import requests
import re

class ExchangeRateApp:

    def __init__(self, root):
        self.root = root
        self.root.title("Exchange Rate Analyzer")
        self.year_var = tk.StringVar()
        self.year_var.set("2022")  # Set a default year

        self.year_label = ttk.Label(root, text="Select Year:")
        self.year_label.grid(row=1, column=2, padx=10, pady=10)

        self.year_dropdown = ttk.Combobox(root, textvariable=self.year_var)
        self.year_dropdown['values'] = [str(year) for year in range(2012, 2023)]  # Add years 2012 to 2022
        self.year_dropdown.grid(row=1, column=3, padx=10, pady=10)
        self.year_dropdown.bind('<<ComboboxSelected>>', self.on_year_select)

        # Load CSV initially for the default year
        self.load_csv_data()

        # UI Components
        self.label_currency1 = ttk.Label(root, text="Currency 1:")
        self.label_currency1.grid(row=0, column=0, padx=10, pady=10)

        # USD is the base currency, so it is auto-populated
        self.currency1 = ttk.Label(root, text="USD")
        self.currency1.grid(row=0, column=1, padx=10, pady=10)

        self.label_currency2 = ttk.Label(root, text="Currency 2:")
        self.label_currency2.grid(row=0, column=2, padx=10, pady=10)

        # Dropdown for selecting Currency 2
        self.currency2_var = tk.StringVar()
        self.currency2_dropdown = ttk.Combobox(root, textvariable=self.currency2_var)
        self.currency2_dropdown['values'] = list(self.df.columns[1:])
        self.currency2_dropdown.grid(row=0, column=3, padx=10, pady=10)

        self.label_duration = ttk.Label(root, text="Duration:")
        self.label_duration.grid(row=1, column=0, padx=10, pady=10)

        # Dropdown for selecting duration (weekly, monthly, quarterly, annual)
        self.duration_var = tk.StringVar()
        self.duration_dropdown = ttk.Combobox(root, textvariable=self.duration_var, values=["Weekly", "Monthly", "Quarterly", "Annual"])
        self.duration_dropdown.grid(row=1, column=1, padx=10, pady=10)

        # Button to plot the chart
        self.plot_button = ttk.Button(root, text="Plot Chart", command=self.plot_chart)
        self.plot_button.grid(row=2, column=0, padx=10, pady=10)

        # Matplotlib figure for displaying the chart
        self.fig = Figure(figsize=(8, 5), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas.get_tk_widget().grid(row=3, column=0, columnspan=4, padx=10, pady=10)

        # Additional UI Components
        # Add a label and entry for amount input
        self.label_amount = ttk.Label(root, text="Amount:")
        self.label_amount.grid(row=6, column=0, padx=10, pady=10)

        self.amount_var = tk.DoubleVar()
        self.amount_entry = ttk.Entry(root, textvariable=self.amount_var)
        self.amount_entry.grid(row=6, column=1, padx=10, pady=10)

        # Add a label for source currency
        self.label_source_currency = ttk.Label(root, text="Source Currency:")
        self.label_source_currency.grid(row=5, column=0, padx=10, pady=10)

        # Dropdown for selecting source currency
        self.source_currency_var = tk.StringVar()
        self.source_currency_dropdown = ttk.Combobox(root, textvariable=self.source_currency_var)
        self.source_currency_dropdown['values'] = list(self.df.columns[1:])
        self.source_currency_dropdown.grid(row=5, column=1, padx=10, pady=10)

        # Add a label for target currency
        self.label_target_currency = ttk.Label(root, text="Target Currency:")
        self.label_target_currency.grid(row=5, column=2, padx=10, pady=10)

        # Dropdown for selecting target currency
        self.target_currency_var = tk.StringVar()
        self.target_currency_dropdown = ttk.Combobox(root, textvariable=self.target_currency_var)
        self.target_currency_dropdown['values'] = list(self.df.columns[1:])
        self.target_currency_dropdown.grid(row=5, column=3, padx=10, pady=10)

        # Add a button for currency conversion
        self.convert_button = ttk.Button(root, text="Convert Currency", command=self.convert_currency)
        self.convert_button.grid(row=6, column=2, padx=10, pady=10)

        # Add a label to display the result
        self.result_label = ttk.Label(root, text="")
        self.result_label.grid(row=6, column=3, padx=10, pady=10)

        # Add a button to view exchange rates
        self.rates_button = ttk.Button(root, text="View Exchange Rates", command=self.show_exchange_rates)
        self.rates_button.grid(row=7, column=0, columnspan=4, padx=10, pady=10)

        # Add a button to view all currencies
        self.all_currencies_button = ttk.Button(root, text="View All Currencies", command=self.show_all_currencies)
        self.all_currencies_button.grid(row=8, column=0, columnspan=4, padx=10, pady=10)

    def on_year_select(self, event):
        # Handle the event when the year dropdown selection changes
        self.load_csv_data()

    def load_csv_data(self):
        selected_year = self.year_var.get()

        # Load the CSV corresponding to the selected year
        csv_file_path = f'Exchange_Rate_Report\Exchange_Rate_Report_{selected_year}.csv'
        self.df = pd.read_csv(csv_file_path)

        # Convert 'Date' column to datetime format
        self.df['Date'] = pd.to_datetime(self.df['Date'], format='%d-%b-%y')

    def plot_chart(self):
        currency2 = self.currency2_var.get()
        duration = self.duration_var.get()

        # Filter data based on selected currency and duration
        filtered_data = self.filter_data(currency2, duration)

        # Find the date when the rate was at its peak and lowest
        peak_date = filtered_data.idxmax()[currency2]
        lowest_date = filtered_data.idxmin()[currency2]

        # Display the dates on the main root window
        root = self.canvas.get_tk_widget().grid_info()['in']
        peak_date_label = ttk
        peak_date_label = ttk.Label(root, text=f"Peak Date: {peak_date}")
        peak_date_label.grid(row=4, column=1, padx=10, pady=10)

        lowest_date_label = ttk.Label(root, text=f"Lowest Date: {lowest_date}")
        lowest_date_label.grid(row=4, column=2, padx=10, pady=10)

        # Plot the chart on the canvas
        self.ax.clear()
        self.ax.plot(filtered_data.index, filtered_data[currency2], marker='o', linestyle='-', color='b')
        self.ax.set_title(f'{currency2} Exchange Rates {duration}')
        self.ax.set_xlabel('Date')
        self.ax.set_ylabel(f'Exchange Rate ({currency2} to USD)')
        self.ax.grid(True)
        self.canvas.draw()

    def filter_data(self, currency2, duration):
        selected_year = self.year_var.get()
        csv_file_path = f'Exchange_Rate_Report\Exchange_Rate_Report_{selected_year}.csv'
        
        # Load data for the selected year
        df = pd.read_csv(csv_file_path)
        df['Date'] = pd.to_datetime(df['Date'], format='%d-%b-%y')

        # Filter data based on selected currency and duration
        if duration == "Weekly":
            filtered_data = df.resample('W-Mon', on='Date').mean()
        elif duration == "Monthly":
            filtered_data = df.resample('M', on='Date').mean()
        elif duration == "Quarterly":
            filtered_data = df.resample('Q', on='Date').mean()
        elif duration == "Annual":
            filtered_data = df.resample('Y', on='Date').mean()
        else:
            # Default to Monthly if an invalid duration is provided
            filtered_data = df.resample('M', on='Date').mean()

        return filtered_data

    def convert_currency(self):
        source_currency = self.source_currency_var.get()
        target_currency = self.target_currency_var.get()

        try:
            amount = float(self.amount_var.get())
        except ValueError:
            # Handle invalid amount input
            self.result_label.configure(text="Invalid amount")
            return

        # Construct the API URL
        match1 = re.search(r'\((\w{3})\)', source_currency)
        currency_source = match1.group(1)
        match = re.search(r'\((\w{3})\)', target_currency)
        currency_code = match.group(1)
        api_url = f"https://api.frankfurter.app/latest?amount={amount}&from={currency_source}&to={currency_code}"

        try:
            # Fetch the conversion rate using the Frankfurter API
            response = requests.get(api_url)
            response.raise_for_status()  # Raise an error for non-200 status codes
            print(response)
            # Extract the converted amount from the JSON response
            exchange_rates = response.json()['rates']
            converted_amount = exchange_rates[currency_code]

            # Display the result
            self.result_label.configure(text=f"{amount:.3f} {source_currency} is {converted_amount:.3f} {target_currency}")

        except requests.RequestException as e:
            # Handle any request-related exceptions
            self.result_label.configure(text=f"Request Error: {e}")
        except (KeyError, ValueError):
            # Handle errors in JSON response
            self.result_label.configure(text="Error fetching conversion rate")

    def show_exchange_rates(self):
        # Create a new window
        rates_window = tk.Toplevel(self.root)
        rates_window.title("Exchange Rates")

        # Fetch exchange rates for USD as base currency
        base_currency = 'USD'
        api_url = f"https://api.frankfurter.app/latest?from={base_currency}"
        response = requests.get(api_url)

        try:
            response.raise_for_status()
            exchange_rates = response.json()['rates']

            # Create and populate a text widget in the new window
            text_widget = tk.Text(rates_window, wrap=tk.WORD, width=40, height=20)
            text_widget.pack()

            # Display exchange rates in the text widget
            text_widget.insert(tk.END, f"Exchange Rates for {base_currency}:\n\n")
            for currency, rate in exchange_rates.items():
                text_widget.insert(tk.END, f"{currency}: {rate:.4f}\n")

        except requests.RequestException as e:
            # Handle any request-related exceptions
            error_label = ttk.Label(rates_window, text=f"Request Error: {e}")
            error_label.pack()

        except (KeyError, ValueError):
            # Handle errors in JSON response
            error_label = ttk.Label(rates_window, text="Error fetching exchange rates")
            error_label.pack()

    def show_all_currencies(self):
        # Create a new window
        currencies_window = tk.Toplevel(self.root)
        currencies_window.title("All Currencies")

        # Fetch all currencies with short code, description, and current exchange rate
        api_url = "https://api.frankfurter.app/latest"
        response = requests.get(api_url)

        try:
            response.raise_for_status()
            all_currencies = response.json()['rates']

            # Create and populate a text widget in the new window
            text_widget = tk.Text(currencies_window, wrap=tk.WORD, width=60, height=20)
            text_widget.pack()

            # Display all currencies in the text widget
            text_widget.insert(tk.END, f"{'Short Code':<15}{'Description':<30}{'Exchange Rate':<15}\n")
            text_widget.insert(tk.END, "="*60 + "\n")
            for currency, rate in all_currencies.items():
                text_widget.insert(tk.END, f"{currency:<15}{self.get_currency_description(currency):<30}{rate:.4f}\n")

        except requests.RequestException as e:
            # Handle any request-related exceptions
            error_label = ttk.Label(currencies_window, text=f"Request Error: {e}")
            error_label.pack()

        except (KeyError, ValueError):
            # Handle errors in JSON response
            error_label = ttk.Label(currencies_window, text="Error fetching currencies")
            error_label.pack()

    def get_currency_description(self, currency_code):
        # Dictionary mapping currency codes to descriptions
        currency_descriptions = {
            'USD': 'United States Dollar',
            'EUR': 'Euro',
            'GBP': 'British Pound Sterling',
            'AUD': 'Australian Dollar',
            'BGN': 'Bulgarian Lev',
            'BRL': 'Brazilian Real',
            'CAD': 'Canadian Dollar',
            'CHF': 'Swiss Franc',
            'CNY': 'Chinese Yuan',
            'CZK': 'Czech Koruna',
            'DKK': 'Danish Krone',
            'HKD': 'Hong Kong Dollar',
            'HUF': 'Hungarian Forint',
            'IDR': 'Indonesian Rupiah',
            'ILS': 'Israeli New Shekel',
            'INR': 'Indian Rupee',
            'ISK': 'Icelandic Króna',
            'JPY': 'Japanese Yen',
            'KRW': 'South Korean Won',
            'MXN': 'Mexican Peso',
            # Add more currency codes and descriptions as needed
        }

        # Return the description for the given currency code
        return currency_descriptions.get(currency_code, currency_code)

if __name__ == "__main__":
    root = tk.Tk()
    app = ExchangeRateApp(root)
    root.mainloop()