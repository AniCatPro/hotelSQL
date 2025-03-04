import sqlite3

conn = sqlite3.connect("hotel1.db")
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS hotels (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT,
                        inn TEXT UNIQUE,
                        director TEXT,
                        owner TEXT,
                        address TEXT,
                        stars INTEGER
                      )''')

cursor.execute('''CREATE TABLE IF NOT EXISTS positions (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT UNIQUE,
                        salary INTEGER
                      )''')

cursor.execute('''CREATE TABLE IF NOT EXISTS staff (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        hotel_id INTEGER,
                        inn TEXT,
                        name TEXT,
                        position_id INTEGER,
                        salary_factor REAL,
                        FOREIGN KEY (hotel_id) REFERENCES hotels(id),
                        FOREIGN KEY (position_id) REFERENCES positions(id)
                      )''')

cursor.execute('''CREATE TABLE IF NOT EXISTS rooms (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        hotel_id INTEGER,
                        description TEXT,
                        places INTEGER,
                        price_per_day INTEGER,
                        status TEXT,
                        FOREIGN KEY (hotel_id) REFERENCES hotels(id)
                      )''')

cursor.execute('''CREATE TABLE IF NOT EXISTS bookings (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        room_id INTEGER,
                        arrival_date TEXT,
                        visitor_info TEXT,
                        FOREIGN KEY (room_id) REFERENCES rooms(id)
                      )''')

cursor.execute('''CREATE TABLE IF NOT EXISTS guests (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        hotel_id INTEGER,
                        room_id INTEGER,
                        check_in_date TEXT,
                        check_out_date TEXT,
                        prepayment INTEGER,
                        visitor_info TEXT,
                        FOREIGN KEY (room_id) REFERENCES rooms(id),
                        FOREIGN KEY (hotel_id) REFERENCES hotels(id)
                      )''')

conn.commit()
conn.close()

print("База данных создана успешно!")
