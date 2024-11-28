import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
from tkinter import Tk, Label, Entry, Button, StringVar, Text, Scrollbar, OptionMenu, messagebox, END


def get_user_function(function_str):
    try:
        x, y = sp.symbols('x y')
        function_sympy = sp.sympify(function_str)
        if not {x, y}.intersection(function_sympy.free_symbols):
            raise ValueError("Функція повинна містити змінні 'x' та/або 'y'.")
        return function_sympy, sp.lambdify((x, y), function_sympy, "numpy")
    except (sp.SympifyError, ValueError) as error:
        messagebox.showerror("Помилка введення", f"Помилка введення: {error}")
        return None, None


def euler_method(f, x0, y0, h, x_end):
    x_values = [x0]
    y_values = [y0]
    x = x0
    y = y0
    while x < x_end:
        y = y + h * f(x, y)
        x = x + h
        x_values.append(x)
        y_values.append(y)
    return x_values, y_values


def euler_cauchy_method(f, x0, y0, h, x_end):
    x_values = [x0]
    y_values = [y0]
    x = x0
    y = y0
    while x < x_end:
        y_temp = y + h * f(x, y)
        y = y + (h / 2) * (f(x, y) + f(x + h, y_temp))
        x = x + h
        x_values.append(x)
        y_values.append(y)
    return x_values, y_values


def calculate():
    function_str = function_input.get()
    method = method_var.get()
    try:
        x0 = float(x0_input.get())
        y0 = float(y0_input.get())
        x_end = float(x_end_input.get())
        h = float(h_input.get())
        if x0 >= x_end:
            messagebox.showerror("Помилка", "Початкове значення x0 має бути меншим за кінцеве x_end.")
            return
        if h <= 0:
            messagebox.showerror("Помилка", "Крок h має бути додатним.")
            return
    except ValueError:
        messagebox.showerror("Помилка", "Введіть коректні числові значення.")
        return

    function_sympy, f = get_user_function(function_str)
    if f is None:
        return

    if method == "Метод Ейлера":
        x_values, y_values = euler_method(f, x0, y0, h, x_end)
    elif method == "Метод Ейлера-Коші":
        x_values, y_values = euler_cauchy_method(f, x0, y0, h, x_end)
    else:
        messagebox.showerror("Помилка", "Оберіть метод розрахунку.")
        return

    output_text.delete(1.0, END)
    output_text.insert(END, "Таблиця значень:\n")
    output_text.insert(END, "x\ty\n")
    output_text.insert(END, "-" * 30 + "\n")
    for x, y in zip(x_values, y_values):
        output_text.insert(END, f"{x:.4f}\t{y:.4f}\n")

    plt.figure(figsize=(8, 6))
    plt.plot(x_values, y_values, marker='o', label="Чисельний розв'язок")
    plt.title("Графік чисельного розв'язку")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.legend()
    plt.grid()
    plt.show()


if __name__ == "__main__":
    root = Tk()
    root.title("Чисельні методи для ОДУ")
    root.geometry("700x700")

    Label(root, text="Введіть функцію y' = f(x, y):").pack()
    function_input = Entry(root, width=50)
    function_input.pack()

    Label(root, text="Введіть початкове значення x0:").pack()
    x0_input = Entry(root, width=20)
    x0_input.pack()

    Label(root, text="Введіть початкове значення y0:").pack()
    y0_input = Entry(root, width=20)
    y0_input.pack()

    Label(root, text="Введіть кінцеве значення x:").pack()
    x_end_input = Entry(root, width=20)
    x_end_input.pack()

    Label(root, text="Введіть крок h:").pack()
    h_input = Entry(root, width=20)
    h_input.pack()

    Label(root, text="Оберіть метод:").pack()
    method_var = StringVar(root)
    method_var.set("Метод Ейлера")
    method_menu = OptionMenu(root, method_var, "Метод Ейлера", "Метод Ейлера-Коші")
    method_menu.pack()

    Button(root, text="Обчислити", command=calculate).pack()

    Label(root, text="Результати:").pack()
    output_text = Text(root, width=80, height=20)
    output_text.pack()

    root.mainloop()
