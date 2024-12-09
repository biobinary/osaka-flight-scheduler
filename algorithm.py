from queue import PriorityQueue
from models import Gate, GateAssignment, db
from datetime import datetime, timedelta

def find_available_gate(arrival_time, departure_time):
    # Fetch all available gates
    gates = Gate.query.all()

    # Iterate through each gate
    for gate in gates:
        # Convert arrival_time and departure_time to datetime objects
        arrival_datetime = datetime.combine(datetime.today(), arrival_time)
        departure_datetime = datetime.combine(datetime.today(), departure_time)

        # Check if the gate has overlapping assignments
        overlapping = GateAssignment.query.filter(
            GateAssignment.gate_id == gate.gate_id,
            db.or_(
                db.and_(GateAssignment.arrival_time <= arrival_datetime, GateAssignment.departure_time > arrival_datetime),
                db.and_(GateAssignment.arrival_time < departure_datetime, GateAssignment.departure_time >= departure_datetime),
                db.and_(GateAssignment.arrival_time >= arrival_datetime, GateAssignment.departure_time <= departure_datetime)
            )
        ).first()

        # Ensure a 30-minute buffer time
        previous_assignment = GateAssignment.query.filter(
            GateAssignment.gate_id == gate.gate_id,
            GateAssignment.departure_time <= arrival_datetime - timedelta(minutes=30)
        ).order_by(GateAssignment.departure_time.desc()).first()

        next_assignment = GateAssignment.query.filter(
            GateAssignment.gate_id == gate.gate_id,
            GateAssignment.arrival_time >= departure_datetime + timedelta(minutes=30)
        ).order_by(GateAssignment.arrival_time.asc()).first()

        if not overlapping and not previous_assignment and not next_assignment:
            return gate.gate_id

    # If no gates are available, return None
    return None
