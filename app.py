import tkinter as tk
from tkinter import ttk
from tkinter import DoubleVar, IntVar
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Load data for height and weight
file_path_height = '/Users/thangnguyenviet/Documents/Python apps/L0_24months.xlsx'
file_path_weight = '/Users/thangnguyenviet/Documents/Python apps/W0_24months.xlsx'
df_height = pd.read_excel(file_path_height)
df_weight = pd.read_excel(file_path_weight)

# Filter data for months 0 to 24
df_height = df_height[(df_height['month'] >= 0) & (df_height['month'] <= 24)]
df_weight = df_weight[(df_weight['month'] >= 0) & (df_weight['month'] <= 24)]

# Tkinter app setup
root = tk.Tk()
root.title("BIỂU ĐỒ TĂNG TRƯỞNG TRẺ 0 -24 THÁNG")

# Gender selection
gender_var = tk.StringVar(value='M')
gender_label = tk.Label(root, text="Select Gender:")
gender_label.pack()
gender_menu = ttk.Combobox(root, textvariable=gender_var, values=['M', 'F'])
gender_menu.pack()

# Data choice selection
data_choice_var = tk.StringVar(value='Height')
data_choice_label = tk.Label(root, text="Select Data Type:")
data_choice_label.pack()
data_choice_menu = ttk.Combobox(root, textvariable=data_choice_var, values=['Height', 'Weight'])
data_choice_menu.pack()

# Month input
month_var = tk.IntVar(value=0)
month_label = tk.Label(root, text="Enter Month to Highlight (0-24):")
month_label.pack()
month_entry = tk.Entry(root, textvariable=month_var)
month_entry.pack()

# Value input
value_var = tk.DoubleVar(value=0.0)
value_label = tk.Label(root, text="Enter Value to Highlight:")
value_label.pack()
value_entry = tk.Entry(root, textvariable=value_var)
value_entry.pack()

# Plot function
def plot_graph():
    data_choice = data_choice_var.get()
    gender_input = gender_var.get()
    
    # Choose the appropriate DataFrame based on selection
    df = df_height if data_choice == 'Height' else df_weight
    df_gender = df[df['gender'] == gender_input]

    # Retrieve values from input fields
    try:
        month_input = month_var.get()
        value_input = value_var.get()
    except tk.TclError:
        tk.messagebox.showerror("Invalid input", "Please enter valid numbers for month and value.")
        return

    # Plotting
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.plot(df_gender['month'], df_gender['SD1'], label='SD1', linestyle=':')
    ax.plot(df_gender['month'], df_gender['SD2'], label='SD2', linestyle='-.')
    ax.plot(df_gender['month'], df_gender['SD3'], label='SD3')
    ax.plot(df_gender['month'], df_gender['SD1neg'], label='-SD1', linestyle=':')
    ax.plot(df_gender['month'], df_gender['SD2neg'], label='-SD2', linestyle='-.')
    ax.plot(df_gender['month'], df_gender['SD3neg'], label='-SD3')

    # Highlighted point
    ax.scatter(month_input, value_input, color='red', s=150, zorder=5, 
               label=f"Selected Point: Month {month_input}, Value {value_input}", marker='*')

    # Grid and labels
    ax.set_xticks(range(0, 25, 1))
    ax.grid(True, which='both', axis='x', linestyle='--', linewidth=0.5)
    ax.set_xlabel('Month')
    ax.set_ylabel(f"{data_choice} Value")
    ax.legend(loc='lower center', bbox_to_anchor=(0.5, -0.2), ncol=7)

    # Clear previous plot if exists
    for widget in plot_frame.winfo_children():
        widget.destroy()

    # Display the plot in Tkinter
    canvas = FigureCanvasTkAgg(fig, master=plot_frame)
    canvas.draw()
    canvas.get_tk_widget().pack()

# Plot button
plot_button = tk.Button(root, text="Plot Growth Chart", command=plot_graph)
plot_button.pack()

# Frame to display the plot
plot_frame = tk.Frame(root)
plot_frame.pack()

root.mainloop()
