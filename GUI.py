import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox

# Подключение к базе данных
conn = sqlite3.connect('hotel.db')
cursor = conn.cursor()

# Создание основного окна
root = tk.Tk()
root.title("Управление гостиницей")

# Функция для отображения данных
def display_data(table):
    # Очищаем предыдущие данные
    for row in treeview.get_children():
        treeview.delete(row)

    query = f"SELECT * FROM {table}"
    cursor.execute(query)
    rows = cursor.fetchall()

    # Заполняем Treeview данными из базы
    for row in rows:
        treeview.insert("", "end", values=row)

# Функция для добавления записи
def add_record():
    def save_record():
        try:
            table = table_var.get()
            if table == "hotels":
                query = "INSERT INTO hotels (name, inn, director, owner, address) VALUES (?, ?, ?, ?, ?)"
                values = (name_entry.get(), inn_entry.get(), director_entry.get(), owner_entry.get(), address_entry.get())
            elif table == "rooms":
                query = "INSERT INTO rooms (hotel_id, description, places, price_per_day, status) VALUES (?, ?, ?, ?, ?)"
                values = (hotel_id_entry.get(), description_entry.get(), places_entry.get(), price_per_day_entry.get(), status_entry.get())

            cursor.execute(query, values)
            conn.commit()
            messagebox.showinfo("Успех", "Запись добавлена!")
            display_data(table)

            add_window.destroy()  # Закрытие окна добавления

        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось добавить запись: {e}")

    add_window = tk.Toplevel(root)
    add_window.title("Добавить запись")

    # Ввод данных для добавления записи
    name_label = tk.Label(add_window, text="Название гостиницы")
    name_label.grid(row=0, column=0)
    name_entry = tk.Entry(add_window)
    name_entry.grid(row=0, column=1)

    inn_label = tk.Label(add_window, text="ИНН")
    inn_label.grid(row=1, column=0)
    inn_entry = tk.Entry(add_window)
    inn_entry.grid(row=1, column=1)

    director_label = tk.Label(add_window, text="Директор")
    director_label.grid(row=2, column=0)
    director_entry = tk.Entry(add_window)
    director_entry.grid(row=2, column=1)

    owner_label = tk.Label(add_window, text="Владелец")
    owner_label.grid(row=3, column=0)
    owner_entry = tk.Entry(add_window)
    owner_entry.grid(row=3, column=1)

    address_label = tk.Label(add_window, text="Адрес")
    address_label.grid(row=4, column=0)
    address_entry = tk.Entry(add_window)
    address_entry.grid(row=4, column=1)

    # Кнопка для сохранения записи
    save_button = tk.Button(add_window, text="Сохранить", command=save_record)
    save_button.grid(row=5, columnspan=2)

# Создание интерфейса для отображения таблицы
table_var = tk.StringVar()
table_var.set("hotels")

# Список таблиц
table_frame = tk.Frame(root)
table_frame.pack(padx=10, pady=10)

hotel_button = tk.Button(table_frame, text="Гостиницы", command=lambda: display_data("hotels"))
hotel_button.grid(row=0, column=0, padx=5)
room_button = tk.Button(table_frame, text="Номера", command=lambda: display_data("rooms"))
room_button.grid(row=0, column=1, padx=5)

# Создание Treeview для отображения данных
treeview = ttk.Treeview(root, columns=("ID", "Name", "INN", "Director", "Owner", "Address"), show="headings")
treeview.pack(padx=10, pady=10)

# Добавление колонок для Treeview
treeview.heading("ID", text="ID")
treeview.heading("Name", text="Name")
treeview.heading("INN", text="INN")
treeview.heading("Director", text="Director")
treeview.heading("Owner", text="Owner")
treeview.heading("Address", text="Address")

# Кнопка для добавления записи
add_button = tk.Button(root, text="Добавить запись", command=add_record)
add_button.pack(padx=10, pady=10)

# Отображаем данные гостиниц по умолчанию
display_data("hotels")

# Запуск основного цикла
root.mainloop()

conn.close()
