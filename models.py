from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Aircraft(db.Model):

    __tablename__ = 'aircraft'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True) 
    aircraft_code = db.Column(db.String(50), unique=True, nullable=False)
    aircraft_name = db.Column(db.String(150), nullable=False)
    airline = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"<Aircraft(id={self.id}, aircraft_code='{self.aircraft_code}', aircraft_name='{self.aircraft_name}', airline='{self.airline}')>"
    
class Flight(db.Model):

    __tablename__ = 'flight'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    flight_number = db.Column(db.String(50), unique=True, nullable=False)
    aircraft_id = db.Column(db.Integer, db.ForeignKey('aircraft.id'), nullable=False)
    origin = db.Column(db.String(100), nullable=False)
    destination = db.Column(db.String(100), nullable=False)
    departure_time = db.Column(db.DateTime, nullable=False)
    arrival_time = db.Column(db.DateTime, nullable=False)
    gate_id = gate_id = db.Column(db.Integer, db.ForeignKey('gate.gate_id'), nullable=True)

    aircraft = db.relationship('Aircraft', backref='flights', lazy=True)
    gate = db.relationship('Gate', backref='flights', lazy=True)

    def __repr__(self):
        return (f"<Flight(id={self.id}, flight_number='{self.flight_number}', aircraft_id={self.aircraft_id}, "
                f"origin='{self.origin}', destination='{self.destination}', "
                f"departure_time='{self.departure_time}', arrival_time='{self.arrival_time}', "
                f"gate='{self.gate_id}')>")
    
class Gate(db.Model):

    __tablename__ = 'gate'
    
    gate_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    gate = db.Column(db.String(50), unique=True, nullable=False)

    def __repr__(self):
        return f"<Gate(gate_id={self.gate_id}, gate='{self.gate}')>"

class GateAssignment(db.Model):

    __tablename__ = 'gate_assignment'

    gate_id = db.Column(db.Integer, db.ForeignKey('gate.gate_id'), nullable=False)
    flight_id = db.Column(db.Integer, db.ForeignKey('flight.id'), nullable=False)
    departure_time = db.Column(db.DateTime, nullable=False)
    arrival_time = db.Column(db.DateTime, nullable=False)

    __table_args__ = (
        db.PrimaryKeyConstraint('gate_id', 'flight_id', name='pk_gate_flight'),
    )

    gate = db.relationship('Gate', backref='assignments', lazy=True)
    flight = db.relationship('Flight', backref='assignments', lazy=True)

    def __repr__(self):
        return (f"<GateAssignment(gate_id={self.gate_id}, flight_id={self.flight_id}, "
                f"departure_time='{self.departure_time}', arrival_time='{self.arrival_time}')>")