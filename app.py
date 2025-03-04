from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import random
import string

app = Flask(__name__, static_folder='img')  # Настроили папку для статичных файлов


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


# Страница регистрации гостя
@app.route('/register_guest', methods=['GET', 'POST'])
def register_guest():
    conn = get_db()
    cursor = conn.cursor()

    # Получаем список всех доступных номеров
    cursor.execute('SELECT * FROM rooms')
    rooms = cursor.fetchall()
    conn.close()

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

    return render_template('register_guest.html', rooms=rooms)


# Страница бронирования
@app.route('/book_room', methods=['GET', 'POST'])
def book_room():
    conn = get_db()
    cursor = conn.cursor()

    # Получаем список всех доступных номеров
    cursor.execute('SELECT * FROM rooms')
    rooms = cursor.fetchall()
    conn.close()

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

    return render_template('book_room.html', rooms=rooms)


# Страница отчетов
@app.route('/reports')
def reports():
    return render_template('reports.html')


# Отчет: Свободные номера на заданную дату
@app.route('/report/available_rooms', methods=['GET'])
def available_rooms_report():
    date = request.args.get('date')

    conn = get_db()
    cursor = conn.cursor()

    # Получаем список свободных номеров на заданную дату
    cursor.execute('''
        SELECT r.id, r.description
        FROM rooms r
        WHERE r.id NOT IN (
            SELECT g.room_id
            FROM guests g
            WHERE (g.check_in_date <= ? AND g.check_out_date >= ?)
        )
    ''', (date, date))
    available_rooms = cursor.fetchall()
    conn.close()

    return render_template('report_available_rooms.html', available_rooms=available_rooms)


# Отчет: Свободные и занятые номера на заданную дату
@app.route('/report/rooms_status', methods=['GET'])
def rooms_status_report():
    date = request.args.get('date')

    conn = get_db()
    cursor = conn.cursor()

    # Получаем список всех номеров и их статус на заданную дату
    cursor.execute('''
        SELECT r.id, r.description,
            CASE 
                WHEN r.id NOT IN (
                    SELECT g.room_id
                    FROM guests g
                    WHERE (g.check_in_date <= ? AND g.check_out_date >= ?)
                )
                THEN 'Свободен'
                ELSE 'Занят'
            END AS status
        FROM rooms r
    ''', (date, date))
    rooms_status = cursor.fetchall()
    conn.close()

    return render_template('report_rooms_status.html', rooms_status=rooms_status)


# Отчет: Количество посетителей в заданный период
@app.route('/report/guests_in_date_range', methods=['GET'])
def guests_in_date_range_report():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    conn = get_db()
    cursor = conn.cursor()

    # Получаем количество гостей, посетивших гостиницу в указанный период
    cursor.execute('''
        SELECT COUNT(*) AS guest_count
        FROM guests g
        WHERE g.check_in_date BETWEEN ? AND ?
    ''', (start_date, end_date))
    guests_count = cursor.fetchone()
    conn.close()

    return render_template('report_guests_in_date_range.html', guests_count=guests_count)


if __name__ == '__main__':
    app.run(debug=True)
