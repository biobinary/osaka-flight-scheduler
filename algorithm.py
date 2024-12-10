from queue import PriorityQueue
from models import Gate, GateAssignment, db
from datetime import datetime, timedelta

def heuristic(gate_id, arrival_time, departure_time):
    conflicts = GateAssignment.query.filter(
        GateAssignment.gate_id == gate_id,
        db.or_(
            db.and_(GateAssignment.arrival_time <= arrival_time, GateAssignment.departure_time > arrival_time),
            db.and_(GateAssignment.arrival_time < departure_time, GateAssignment.departure_time >= departure_time),
            db.and_(GateAssignment.arrival_time >= arrival_time, GateAssignment.departure_time <= departure_time)
        )
    ).count()
    return conflicts

def find_available_gate(arrival_time, departure_time):
    gates = Gate.query.all()
    pq = PriorityQueue()

    for gate in gates:
        priority = heuristic(gate.gate_id, arrival_time, departure_time)
        pq.put((priority, gate.gate_id))

    while not pq.empty():
        _, gate_id = pq.get()

        overlapping = GateAssignment.query.filter(
            GateAssignment.gate_id == gate_id,
            db.or_(
                db.and_(GateAssignment.arrival_time <= arrival_time, GateAssignment.departure_time > arrival_time),
                db.and_(GateAssignment.arrival_time < departure_time, GateAssignment.departure_time >= departure_time),
                db.and_(GateAssignment.arrival_time >= arrival_time, GateAssignment.departure_time <= departure_time)
            )
        ).first()

        if not overlapping:
            return gate_id

    return None