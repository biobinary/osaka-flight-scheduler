from queue import PriorityQueue
from models import Gate, GateAssignment, db
from datetime import datetime, timedelta

def find_available_gate(arrival_time, departure_time):
    # Fetch all available gates
    gates = Gate.query.all()

    # Iterate through each gate
    for gate in gates:
        # Check if the gate has overlapping assignments
        overlapping = GateAssignment.query.filter(
            GateAssignment.gate_id == gate.gate_id,
            db.or_(
                db.and_(GateAssignment.arrival_time <= arrival_time, GateAssignment.departure_time > arrival_time),
                db.and_(GateAssignment.arrival_time < departure_time, GateAssignment.departure_time >= departure_time),
                db.and_(GateAssignment.arrival_time >= arrival_time, GateAssignment.departure_time <= departure_time)
            )
        ).first()

        # If no overlap is found, assign the gate
        if not overlapping:
            return gate.gate_id

    # If no gates are available, return None
    return None