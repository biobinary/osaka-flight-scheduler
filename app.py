from flask import Flask, render_template, redirect, request, url_for
from datetime import time, datetime, timedelta
import sqlite3

app = Flask(__name__)

def generate_time_slots(start, end, interval_minutes):
    
    slots = []
    current_time = datetime.strptime(start, '%H:%M')
    end_time = datetime.strptime(end, '%H:%M')
    
    while current_time <= end_time:
        next_time = current_time + timedelta(minutes=interval_minutes - 1)
        slot = f"{current_time.strftime('%H:%M')} - {next_time.strftime('%H:%M')}"
        slots.append(slot)
        current_time = next_time + timedelta(minutes=1)
    
    return slots

@app.route('/', methods=["GET", "POST"])
def home():

    if request.method == 'POST':
        
        departure_time = request.form['departure_time']
        destination = request.form['destination']
        airline = request.form['airline']
        flight_code = request.form['flight_code']
        gate = request.form['gate']
        
        conn = sqlite3.connect('flights.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO flights (departure_time, destination, airline, flight_code, gate)
            VALUES (?, ?, ?, ?, ?)
        ''', (departure_time, destination, airline, flight_code, gate))
        conn.commit()
        conn.close()
        
        return redirect(url_for('home'))

    time_slots = generate_time_slots("07:00", "20:00", 60)
    return render_template('index.html', time_slots=time_slots)

@app.route('/view_flights')
def view_flights():
    conn = sqlite3.connect('flights.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM flights")
    flights = cursor.fetchall()
    conn.close()
    
    return render_template('view_flights.html', flights=flights)

if __name__ == '__main__':
    app.run(debug=True)