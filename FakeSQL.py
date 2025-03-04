import sqlite3
import random
from faker import Faker
import datetime
import os

fake = Faker('ru_RU')

# Функция для генерации ИНН для физических лиц
def generate_inn_physical():
    region_code = random.randint(1, 99)  # Код региона (2 цифры)
    unique_code = random.randint(100000000, 999999999)  # Уникальный код (9 цифр)
    control_number = random.randint(10, 99)  # Контрольное число (2 цифры)
    inn = f"{region_code:02d}{unique_code:09d}{control_number:02d}"
    return inn

# Функция для генерации ИНН для юридических лиц
def generate_inn_legal():
    tax_code = random.randint(1000, 9999)  # Код налогового органа (4 цифры)
    unique_code = random.randint(100000000, 999999999)  # Уникальный код организации (6-8 цифр)
    control_number = random.randint(10, 99)  # Контрольное число (2 цифры)
    inn = f"{tax_code}{unique_code:08d}{control_number:02d}"  # ИНН может быть 10 или 12 цифр
    return inn

# Функция для генерации данных для таблицы гостиниц
def generate_hotels(cursor, num_hotels=10):
    hotels = []
    for _ in range(num_hotels):
        name = fake.company()
        inn = generate_inn_legal()
        director = fake.name()
        owner = fake.name()
        address = fake.address()
        stars = random.randint(1, 5)  # Случайное количество звезд
        hotel = (name, inn, director, owner, address, stars)
        hotels.append(hotel)

    cursor.executemany("INSERT INTO hotels (name, inn, director, owner, address, stars) VALUES (?, ?, ?, ?, ?, ?)", hotels)

# Функция для генерации данных для должностей
def generate_positions(cursor):
    positions = [
        ('Директор', 50000),
        ('Менеджер', 30000),
        ('Уборщица', 20000),
        ('Портье', 25000),
        ('Шеф-повар', 40000)
    ]
    cursor.executemany("INSERT INTO positions (name, salary) VALUES (?, ?)", positions)

# Функция для генерации персонала
def generate_staff(cursor, num_hotels=10):
    staff = []
    for _ in range(num_hotels):
        hotel_id = random.randint(1, num_hotels)
        inn = generate_inn_physical()
        name = fake.name()
        position_id = random.randint(1, 5)
        salary_factor = random.uniform(1.0, 2.0)  # Коэффициент оклада (не более 2)
        staff_member = (hotel_id, inn, name, position_id, salary_factor)
        staff.append(staff_member)

    cursor.executemany("INSERT INTO staff (hotel_id, inn, name, position_id, salary_factor) VALUES (?, ?, ?, ?, ?)", staff)

# Генерация данных для номеров
def generate_rooms(cursor):
    hotels_count = cursor.execute("SELECT COUNT(*) FROM hotels").fetchone()[0]
    rooms = []

    room_types = ["Стандартный", "Люкс", "Эконом"]
    room_sizes = ["Маленький", "Средний", "Большой"]
    bed_types = ["Односпальная", "Двуспальная", "Раскладушка", "Кровать с балдахином"]
    max_occupancy = [2, 3, 4, 5]  # максимальное количество человек
    floor_levels = [1, 2, 3, 4, 5]  # этаж
    views = ["на город", "на парк", "на море"]
    amenities = ["с кондиционером", "с балконом", "с телевизором", "с мини-баром", "с холодильником", "с Wi-Fi"]
    statuses = ["Работает", "На ремонте"]

    for hotel_id in range(1, hotels_count + 1):
        for _ in range(5):  # 5 номеров на каждую гостиницу
            room_type = random.choice(room_types)
            room_size = random.choice(room_sizes)
            bed_type = random.choice(bed_types)
            occupancy = random.choice(max_occupancy)
            floor = random.choice(floor_levels)
            view = random.choice(views)
            room_amenities = random.sample(amenities, 2)
            status = random.choice(statuses)

            description = f"{room_size} {room_type} номер, {bed_type} кровать, максимальное количество: {occupancy} человек, " \
                          f"этаж {floor}, вид: {view}, удобства: " + ", ".join(room_amenities)

            rooms.append((hotel_id, description, occupancy, fake.random_int(min=1000, max=5000), status))

    cursor.executemany("INSERT INTO rooms (hotel_id, description, places, price_per_day, status) VALUES (?, ?, ?, ?, ?)", rooms)

# Функция для генерации данных для бронирований
def generate_bookings(cursor, num_rooms=10):
    bookings = []
    for _ in range(num_rooms):
        room_id = random.randint(1, num_rooms)
        arrival_date = fake.date_this_year()
        visitor_info = fake.name()
        booking = (room_id, arrival_date, visitor_info)
        bookings.append(booking)

    cursor.executemany("INSERT INTO bookings (room_id, arrival_date, visitor_info) VALUES (?, ?, ?)", bookings)

# Функция для генерации данных для гостей
def generate_guests(cursor, num_rooms=10):
    guests = []
    rooms = cursor.execute("SELECT id, hotel_id FROM rooms").fetchall()

    for _ in range(num_rooms):
        room = random.choice(rooms)  # Случайный выбор номера
        room_id = room[0]
        hotel_id = room[1]  # Извлекаем hotel_id для этого номера

        check_in_date = fake.date_this_year()
        check_out_date = str(fake.date_between(start_date=check_in_date, end_date="+10d"))
        prepayment = random.randint(1000, 5000)
        visitor_info = fake.name()

        guest = (hotel_id, room_id, check_in_date, check_out_date, prepayment, visitor_info)
        guests.append(guest)

    cursor.executemany("INSERT INTO guests (hotel_id, room_id, check_in_date, check_out_date, prepayment, visitor_info) VALUES (?, ?, ?, ?, ?, ?)", guests)

# Подключаемся к базе данных и создаем таблицы
def create_tables():
    # Удаляем старую базу данных, если она существует
    if os.path.exists('fake_hotel.db'):
        os.remove('fake_hotel.db')

    connection = sqlite3.connect('fake_hotel.db')
    cursor = connection.cursor()

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

    # Генерация данных
    generate_hotels(cursor)
    generate_positions(cursor)
    generate_staff(cursor)
    generate_rooms(cursor)
    generate_bookings(cursor)
    generate_guests(cursor)

    connection.commit()
    connection.close()
    print("Таблицы созданы и данные загружены!")

create_tables()
