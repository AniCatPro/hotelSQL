import sqlite3

# Подключаемся к базе данных (файл создастся автоматически, если его нет)
conn = sqlite3.connect("hotel.db")
cursor = conn.cursor()

# Создаем таблицу "Гостиницы"
cursor.execute("""
CREATE TABLE IF NOT EXISTS hotels (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    inn TEXT UNIQUE NOT NULL,
    director TEXT,
    owner TEXT,
    address TEXT
);
""")

# Создаем таблицу "Должности"
cursor.execute("""
CREATE TABLE IF NOT EXISTS positions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL
);
""")

# Создаем таблицу "Персонал"
cursor.execute("""
CREATE TABLE IF NOT EXISTS staff (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    hotel_id INTEGER NOT NULL,
    inn TEXT UNIQUE NOT NULL,
    full_name TEXT NOT NULL,
    position_id INTEGER NOT NULL,
    FOREIGN KEY (hotel_id) REFERENCES hotels (id) ON DELETE CASCADE,
    FOREIGN KEY (position_id) REFERENCES positions (id) ON DELETE CASCADE
);
""")

# Создаем таблицу "Номера"
cursor.execute("""
CREATE TABLE IF NOT EXISTS rooms (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    hotel_id INTEGER NOT NULL,
    description TEXT,
    places INTEGER CHECK (places > 0),
    price_per_day REAL CHECK (price_per_day >= 0),
    status TEXT CHECK (status IN ('Работает', 'Ремонт')),
    FOREIGN KEY (hotel_id) REFERENCES hotels (id) ON DELETE CASCADE
);
""")

# Создаем таблицу "Посетители"
cursor.execute("""
CREATE TABLE IF NOT EXISTS guests (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    room_id INTEGER NOT NULL,
    check_in_date DATE,
    check_out_date DATE,
    prepayment REAL CHECK (prepayment >= 0),
    visitor_info TEXT,
    FOREIGN KEY (room_id) REFERENCES rooms (id) ON DELETE CASCADE
);
""")

# Создаем таблицу "Бронь"
cursor.execute("""
CREATE TABLE IF NOT EXISTS bookings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    room_id INTEGER NOT NULL,
    arrival_date DATE,
    visitor_info TEXT,
    FOREIGN KEY (room_id) REFERENCES rooms (id) ON DELETE CASCADE
);
""")

# Сохраняем изменения и закрываем соединение
conn.commit()
conn.close()

print("База данных создана успешно!")
