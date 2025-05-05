import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from tkinter import Tk, filedialog, Label, Button, StringVar, OptionMenu, Frame, Toplevel, Canvas
from tkinter import messagebox, ttk, font
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Global variable to store the dataframe
df = None

def load_csv():
    """
    Load the CSV file via a file dialog and display basic data.
    """
    global df
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if file_path:
        try:
            df = pd.read_csv(file_path)
            status_label.config(text=f"Loaded: {file_path.split('/')[-1]}")
            show_preview()
            update_dropdowns()
            update_table_view()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load file: {e}")

def show_preview():
    """
    Display first few rows and summary statistics.
    """
    if df is not None:
        print("\n--- First 5 Rows ---")
        print(df.head())
        print("\n--- Summary ---")
        print(df.describe())
        print("\n--- Missing Values ---")
        print(df.isnull().sum())

def plot_histograms():
    """
    Generate histograms for numerical columns.
    """
    if df is not None:
        fig, ax = plt.subplots(figsize=(10, 8))
        df.select_dtypes(include='number').hist(ax=ax, bins=10)
        ax.set_title("Histograms of Numerical Data")
        show_plot_in_new_window(fig)

def plot_heatmap():
    """
    Generate a heatmap of the correlations between numerical columns.
    """
    if df is not None:
        fig, ax = plt.subplots(figsize=(10, 6))
        numeric = df.select_dtypes(include='number')
        sns.heatmap(numeric.corr(), annot=True, cmap='coolwarm', fmt=".2f", ax=ax)
        ax.set_title("Correlation Heatmap")
        show_plot_in_new_window(fig)

def plot_pairplot():
    """
    Generate pairplot for numerical data.
    """
    if df is not None:
        fig, ax = plt.subplots(figsize=(10, 8))
        sns.pairplot(df.select_dtypes(include='number'))
        plt.suptitle("Pairplot", y=1.02)
        show_plot_in_new_window(fig)

def plot_custom():
    """
    Generate custom charts (bar, line, scatter, or pie).
    """
    if df is not None:
        x = x_var.get()
        y = y_var.get()
        chart_type = chart_var.get()

        fig, ax = plt.subplots(figsize=(8, 6))
        try:
            if chart_type == 'bar':
                sns.barplot(x=x, y=y, data=df, ax=ax)
            elif chart_type == 'line':
                sns.lineplot(x=x, y=y, data=df, ax=ax)
            elif chart_type == 'scatter':
                sns.scatterplot(x=x, y=y, data=df, ax=ax)
            elif chart_type == 'pie':
                df[x].value_counts().plot.pie(autopct='%1.1f%%', ax=ax)
            ax.set_title(f"{chart_type.title()} Chart")
            plt.xticks(rotation=45)
            show_plot_in_new_window(fig)
        except Exception as e:
            messagebox.showerror("Error", f"Error generating chart: {e}")

def show_plot_in_new_window(fig):
    """
    Show the plot in a new window.
    """
    plot_window = Toplevel(root)
    plot_window.title("Plot")
    plot_window.geometry("800x600")

    canvas = FigureCanvasTkAgg(fig, master=plot_window)
    canvas.get_tk_widget().pack(fill="both", expand=True)
    canvas.draw()

def save_plot():
    """
    Save the currently generated plot as an image.
    """
    if df is not None:
        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", ".png"), ("JPEG files", ".jpg"), ("All files", ".")])
        if file_path:
            plt.savefig(file_path)
            messagebox.showinfo("Success", f"Plot saved as {file_path}")

def clear_data():
    """
    Clear the loaded dataset and reset the interface.
    """
    global df
    df = None
    status_label.config(text="No file loaded")
    messagebox.showinfo("Cleared", "Data cleared. You can load a new file.")
    update_table_view()

def update_dropdowns():
    """
    Update dropdown menus for columns to plot.
    """
    if df is not None:
        cols = list(df.columns)
        x_var.set(cols[0])
        y_var.set(cols[1] if len(cols) > 1 else cols[0])

        x_menu['menu'].delete(0, 'end')
        y_menu['menu'].delete(0, 'end')
        for col in cols:
            x_menu['menu'].add_command(label=col, command=lambda value=col: x_var.set(value))
            y_menu['menu'].add_command(label=col, command=lambda value=col: y_var.set(value))

def update_table_view():
    """
    Update the displayed data table.
    """
    # Clear previous table view
    for widget in table_frame.winfo_children():
        widget.destroy()

    if df is not None:
        cols = list(df.columns)
        table = ttk.Treeview(table_frame, columns=cols, show='headings')

        for col in cols:
            table.heading(col, text=col)

        for _, row in df.iterrows():
            table.insert("", "end", values=list(row))

        table.grid(row=0, column=0, padx=10, pady=10)

# GUI setup
root = Tk()
root.title("CSV Data Visualizer")
root.geometry("900x700")
root.config(bg="#F0F0F0")

# Modern font style
font_style = font.Font(family="Helvetica", size=12, weight="bold")

# Color Scheme
bg_color = "#F0F0F0"  # Light background color
button_color = "#4CAF50"  # Green buttons
hover_color = "#45a049"  # Hover color
button_text_color = "white"

# Main Frames
main_frame = Frame(root, bg=bg_color)
main_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)

# Ensure the rows and columns resize with the window
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)
main_frame.grid_rowconfigure(0, weight=1)
main_frame.grid_columnconfigure(0, weight=1)

# Status Label
status_label = Label(main_frame, text="No file loaded", fg="blue", font=("Arial", 12), bg=bg_color)
status_label.grid(row=0, column=0, columnspan=4, pady=5)

# Buttons
button_frame = Frame(main_frame, bg=bg_color)
button_frame.grid(row=1, column=0, columnspan=4, pady=10)

# Function to change button color on hover
def on_enter(event, button):
    button.config(bg=hover_color)

def on_leave(event, button):
    button.config(bg=button_color)

def create_button(parent, text, command, row, column):
    button = Button(parent, text=text, command=command, width=20, height=2, bg=button_color, fg=button_text_color, font=font_style, relief="flat")
    button.grid(row=row, column=column, padx=10, pady=10)
    button.bind("<Enter>", lambda event, btn=button: on_enter(event, btn))
    button.bind("<Leave>", lambda event, btn=button: on_leave(event, btn))

create_button(button_frame, "Open CSV File", load_csv, 0, 0)
create_button(button_frame, "Show Histograms", plot_histograms, 0, 1)
create_button(button_frame, "Show Heatmap", plot_heatmap, 1, 0)
create_button(button_frame, "Show Pairplot", plot_pairplot, 1, 1)

# Dropdowns for custom plot
chart_frame = Frame(main_frame, bg=bg_color)
chart_frame.grid(row=2, column=0, columnspan=4, pady=10)

Label(chart_frame, text="X Column:", font=font_style, bg=bg_color).grid(row=0, column=0, padx=10, pady=5, sticky="w")
x_var = StringVar(root)
x_menu = OptionMenu(chart_frame, x_var, "")
x_menu.grid(row=0, column=1, padx=10, pady=5)

Label(chart_frame, text="Y Column:", font=font_style, bg=bg_color).grid(row=1, column=0, padx=10, pady=5, sticky="w")
y_var = StringVar(root)
y_menu = OptionMenu(chart_frame, y_var, "")
y_menu.grid(row=1, column=1, padx=10, pady=5)

Label(chart_frame, text="Chart Type:", font=font_style, bg=bg_color).grid(row=2, column=0, padx=10, pady=5, sticky="w")
chart_var = StringVar(root)
chart_var.set("bar")
chart_type_menu = OptionMenu(chart_frame, chart_var, "bar", "line", "scatter", "pie")
chart_type_menu.grid(row=2, column=1, padx=10, pady=5)

create_button(chart_frame, "Plot Custom Chart", plot_custom, 3, 0)

# Saving & Clearing Data
create_button(button_frame, "Save Plot", save_plot, 2, 0)
create_button(button_frame, "Clear Data", clear_data, 2, 1)

# Table Frame for displaying data
table_frame = Frame(main_frame, bg=bg_color)
table_frame.grid(row=3, column=0, columnspan=4, pady=20, sticky="nsew")

root.mainloop()
