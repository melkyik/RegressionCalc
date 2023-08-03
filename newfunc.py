import math
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
from tkinter import scrolledtext

def exponential_power_func(x, B0, B1, B2):
    return B0 * np.exp(B1 * x) * x**B2

def fit_power_regression(data):
    Slny, Slnx, Slnxlny, Slnx2 = 0, 0, 0, 0
    NumValidPoints = 0

    for x, y in data:
        if x != 0:
            ln_y = math.log(y)
            ln_x = math.log(x)
            Slny += ln_y
            Slnx += ln_x
            Slnxlny += ln_x * ln_y
            Slnx2 += ln_x ** 2
            NumValidPoints += 1

    B1 = (NumValidPoints * Slnxlny - Slnx * Slny) / (NumValidPoints * Slnx2 - Slnx ** 2)
    B0 = math.exp((Slny - B1 * Slnx) / NumValidPoints)

    return B0, B1

def fit_polynomial_regression(data, degree):
    x_values = [point[0] for point in data]
    y_values = [point[1] for point in data]
    coefficients = np.polyfit(x_values, y_values, degree)
    return coefficients

def fit_exponential_power_regression(data):
    x_values = [point[0] for point in data]
    y_values = [point[1] for point in data]
    popt, _ = curve_fit(exponential_power_func, x_values, y_values, maxfev=10000)
    return popt

def calculate_and_plot():
    data = []
    for row in data_entries:
        try:
            x = float(row[0].get())
            y = float(row[1].get())-float(ECOsmosEntry.get())
            data.append((x, y))
        except ValueError:
            continue

    if len(data) > 0:
        B0, B1 = fit_power_regression(data)
        polynomial_degree = int(degree_entry.get())
        polynomial_coefficients = fit_polynomial_regression(data, polynomial_degree)
        exponential_power_coefficients = fit_exponential_power_regression(data)

        result_text = f"Результаты степенной регрессии Y=B0*X^B1:\nB0:\t{B0:.10f}\nB1:\t{B1:.10f}\n\n"
  
        result_text += f"Экспоненциально-степенная регрессия Y=B0*Exp(x*B1)*X^B2:\nB0:\t{exponential_power_coefficients[0]:.10f} \nB1:\t{exponential_power_coefficients[1]:.10f} \nB2:\t{exponential_power_coefficients[2]:.10f}"
        polynomial_str = " + ".join([f"{coeff:.5f} * x^{i}" for i, coeff in enumerate(polynomial_coefficients[::-1])])
        result_text += f"\n\nПолином {polynomial_degree} степени:\n{polynomial_str}\n\n"
        result_window = tk.Toplevel(app)
        result_window.title("Результаты")
        result_window.geometry("600x300")

        result_textbox = scrolledtext.ScrolledText(result_window, wrap=tk.WORD, width=150, height=20)
        result_textbox.pack(padx=10, pady=10)
        result_textbox.insert(tk.END, result_text)
        #x_fit = np.linspace(0.1, max(data, key=lambda x: x[0])[0], 100)
        x_fit = np.linspace(0.1, float(xmaxEntry.get()), 100)
        if drawPow.get():
            y_fit_power = [B0 * (x ** B1) for x in x_fit]
            plt.plot(x_fit, y_fit_power, label="Степенная регрессия", color='red')
        if drawpoly.get():
            y_fit_polynomial = np.polyval(polynomial_coefficients, x_fit)
            plt.plot(x_fit, y_fit_polynomial, label=f"Полином {polynomial_degree} степени", color='green')
        if drawExpp.get():
            y_fit_exponential_power = exponential_power_func(x_fit, *exponential_power_coefficients)
            plt.plot(x_fit, y_fit_exponential_power, label="Экспоненциально-степенная функция", color='blue')

        # Построение графика данных
        x_values = [point[0] for point in data]
        y_values = [point[1] for point in data]
        plt.scatter(x_values, y_values, label="Исходные данные")

        plt.xlabel('x')
        plt.ylabel('y')
        plt.legend()
        plt.grid(True)
        plt.show()

# Создание интерфейса
app = tk.Tk()
app.title("Регрессия")

data_entries = []
default_data = [
    (0.1, 36),
    (0.2, 65),
    (0.3, 96),
    (0.4, 122),
    (0.5, 149),
    (0.6, 175),
    (0.7, 201),
    (0.8, 224),
    (0.9, 251),
    (1, 273),
    (2, 524),
    (3, 754),
    (4, 980),
    (5, 1203),
    (6, 1442),
     (7, 1676),
     (8, 1913)
]
row_num = 0
ECOsmosLabel = ttk.Label(app, text="Значение EC осмоса :")
ECOsmosLabel.grid(row=row_num, column=0, padx=2, pady=2)

ECOsmosEntry = tk.Entry(app, width=15)
ECOsmosEntry.grid(row=row_num, column=1, padx=2, pady=2)
ECOsmosEntry.insert(0, str(0))
row_num += 1
for i in range(20):
    x_entry = tk.Entry(app, width=15)
    y_entry = tk.Entry(app, width=15)
    x_entry.grid(row=row_num, column=0, padx=5, pady=2)
    y_entry.grid(row=row_num, column=1, padx=5, pady=2)

    if i < len(default_data):
        x_entry.insert(0, str(default_data[i][0]))
        y_entry.insert(0, str(default_data[i][1]))

    data_entries.append((x_entry, y_entry))
    row_num += 1

degree_label = ttk.Label(app, text="Степень полинома:")
degree_label.grid(row=row_num, column=0, padx=5, pady=5)
degree_entry = tk.Entry(app, width=10)
degree_entry.grid(row=row_num, column=1, padx=5, pady=5)
degree_entry.insert(0, "3")  # По умолчанию степень полинома = 3
row_num += 1

drawpoly=tk.IntVar(value=1)
drawExpp=tk.IntVar(value=1)
drawPow= tk.IntVar(value=1)
cbpoly = tk.Checkbutton(app, text="Рисовать полином", variable=drawpoly, onvalue=1, offvalue=0)
cbexpp = tk.Checkbutton(app, text="Рисовать Эксп.-степенную функцию", variable=drawExpp, onvalue=1, offvalue=0)
cbpow = tk.Checkbutton(app, text="Рисовать степенную функцию", variable=drawPow, onvalue=1, offvalue=0)
cbpoly.grid(row=row_num, column=0, padx=5, pady=1,sticky='w',columnspan=2)
cbexpp.grid(row=row_num+1, column=0, padx=5, pady=1,sticky='w',columnspan=2)
cbpow.grid(row=row_num+2, column=0, padx=5, pady=1,sticky='w',columnspan=2)
row_num += 3

xmaxLabel = ttk.Label(app, text="Max X:")
xmaxLabel.grid(row=row_num+1, column=0, padx=2, pady=2)

xmaxEntry = tk.Entry(app, width=15)
xmaxEntry.grid(row=row_num+1, column=1, padx=2, pady=2)
xmaxEntry.insert(0, str(max(default_data, key=lambda x: x[0])[0],))

calculate_button = ttk.Button(app, text="Рассчитать и построить график", command=calculate_and_plot)
calculate_button.grid(row=row_num+2, column=0, columnspan=2, padx=5, pady=10)


app.mainloop()