from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import random
import string

app = Flask(__name__)


# Функция для подключения к базе данных
def get_db():
    conn = sqlite3.connect('hotel.db')
    conn.row_factory = sqlite3.Row
    return conn


# Главная страница
@app.route('/')
def index():
    return render_template('index.html')


# Страница добавления гостиницы
@app.route('/add_hotel', methods=['GET', 'POST'])
def add_hotel():
    if request.method == 'POST':
        name = request.form['name']
        inn = request.form['inn']
        director = request.form['director']
        owner = request.form['owner']
        address = request.form['address']
        stars = request.form['stars']

        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO hotels (name, inn, director, owner, address, stars)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (name, inn, director, owner, address, stars))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    return render_template('add_hotel.html')


# Страница добавления гостя
@app.route('/add_guest', methods=['GET', 'POST'])
def add_guest():
    if request.method == 'POST':
        room_id = request.form['room_id']
        check_in_date = request.form['check_in_date']
        check_out_date = request.form['check_out_date']
        prepayment = request.form['prepayment']
        visitor_info = request.form['visitor_info']

        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO guests (room_id, check_in_date, check_out_date, prepayment, visitor_info)
            VALUES (?, ?, ?, ?, ?)
        ''', (room_id, check_in_date, check_out_date, prepayment, visitor_info))
        conn.commit()
        conn.close()
        return redirect(url_for('guests_list'))

    return render_template('add_guest.html')


# Страница списка гостей
@app.route('/guests_list')
def guests_list():
    conn = get_db()
    cursor = conn.cursor()

    # Получаем список всех гостей, включая данные о номере (room_id) и описании номера
    cursor.execute('''
        SELECT g.id, r.id, g.check_in_date, g.check_out_date, g.prepayment, g.visitor_info, r.description
        FROM guests g
        JOIN rooms r ON g.room_id = r.id
    ''')
    guests = cursor.fetchall()
    conn.close()

    return render_template('guests_list.html', guests=guests)


# Страница добавления номера
@app.route('/add_room', methods=['GET', 'POST'])
def add_room():
    if request.method == 'POST':
        hotel_id = request.form['hotel_id']
        description = request.form['description']
        places = request.form['places']
        price_per_day = request.form['price_per_day']
        status = request.form['status']

        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO rooms (hotel_id, description, places, price_per_day, status)
            VALUES (?, ?, ?, ?, ?)
        ''', (hotel_id, description, places, price_per_day, status))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    return render_template('add_room.html')


# Страница добавления бронирования
@app.route('/add_booking', methods=['GET', 'POST'])
def add_booking():
    if request.method == 'POST':
        room_id = request.form['room_id']
        arrival_date = request.form['arrival_date']
        visitor_info = request.form['visitor_info']

        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO bookings (room_id, arrival_date, visitor_info)
            VALUES (?, ?, ?)
        ''', (room_id, arrival_date, visitor_info))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    return render_template('add_booking.html')


if __name__ == '__main__':
    app.run(debug=True)
