import tkinter as tk

def move_to_next_entry(event):
    # Получение текущего виджета, на котором было событие
    current_widget = app.focus_get()

    # Переключение фокуса на следующий элемент y_entry
    for x_entry, y_entry in data_entries:
        if current_widget == y_entry:
            index = data_entries.index((x_entry, y_entry))
            if index + 1 < len(data_entries):
                next_y_entry = data_entries[index + 1][1]
                next_y_entry.focus()
            break

app = tk.Tk()
app.title("Регрессия")

row_num = 0
default_data = [(1, 2), (3, 4), (5, 6)]

data_entries = []

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

    # Привязка события для перехода к следующему y_entry при нажатии Enter в y_entry
    y_entry.bind('<Return>', move_to_next_entry)

app.mainloop()