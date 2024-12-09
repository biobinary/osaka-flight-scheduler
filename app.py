from flask import Flask, render_template, redirect, request, url_for, flash
from datetime import datetime
from config import Config
from models import db, Aircraft, Flight, Gate, GateAssignment
from algorithm import find_available_gate

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

@app.route('/')
def home():
    flights = Flight.query.all()
    return render_template('homepage.html', flights=flights)

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        criteria = request.form['criteria']
        value = request.form['value']
        results = []

        if criteria == "origin":
            results = Flight.query.filter(Flight.origin.ilike(f"%{value}%")).all()

        elif criteria == "destination":
            results = Flight.query.filter(Flight.destination.ilike(f"%{value}%")).all()

        elif criteria == "departure_time":
            try:
                time_value = datetime.strptime(value, '%H:%M').time()
                results = Flight.query.filter(
                    db.func.time(Flight.departure_time) == time_value
                ).all()
            except ValueError:
                flash("Invalid time format. Use HH:MM.", "danger")
                results = []

        elif criteria == "aircraft":
            results = Flight.query.filter(Flight.aircraft_id == value).all()

        return render_template('search.html', flights=results)

    return render_template('search.html', flights=[])

@app.route('/add', methods=['GET', 'POST'])
def add_flight():
    if request.method == 'POST':
        flight_number = request.form['flight_number']
        origin = request.form['origin']
        destination = request.form['destination']
        departure_time = datetime.strptime(request.form['departure_time'], '%H:%M').time()
        arrival_time = datetime.strptime(request.form['arrival_time'], '%H:%M').time()
        aircraft_id = request.form['aircraft_id']

        gate_id = find_available_gate(arrival_time, departure_time)
        if gate_id is None:
            flash("No available gate for this flight schedule.", "error")
            return redirect(url_for('add_flight'))

        flight = Flight(
            flight_number=flight_number,
            origin=origin,
            destination=destination,
            departure_time=departure_time,
            arrival_time=arrival_time,
            gate_id=gate_id,
            aircraft_id=aircraft_id
        )
        db.session.add(flight)
        db.session.commit()

        gate_assignment = GateAssignment(
            gate_id=gate_id,
            flight_id=flight.id,
            arrival_time=arrival_time,
            departure_time=departure_time
        )
        db.session.add(gate_assignment)
        db.session.commit()

        flash("Flight added successfully and assigned to gate.", "success")
        return redirect(url_for('home'))
    
    aircrafts = Aircraft.query.all()
    return render_template('add_flight.html', aircrafts=aircrafts)

if __name__ == '__main__':
    app.run(debug=True)