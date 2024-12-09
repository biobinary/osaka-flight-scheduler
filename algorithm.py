from queue import PriorityQueue
from models import Gate, GateAssignment, db

def find_available_gate(start_time, end_time):

    gates = Gate.query.all()
    pq = PriorityQueue()

    def calculate_heuristic(gate):
        return GateAssignment.query.filter(GateAssignment.gate_id == gate.gate_id).count()

    for gate in gates:
        score = calculate_heuristic(gate)
        pq.put((score, gate))

    while not pq.empty():
        _, gate = pq.get() 
        overlapping = GateAssignment.query.filter(
            GateAssignment.gate_id == gate.gate_id,
            db.or_(
                db.and_(GateAssignment.departure_time <= start_time, GateAssignment.arrival_time > start_time),
                db.and_(GateAssignment.departure_time < end_time, GateAssignment.arrival_time >= end_time),
                db.and_(GateAssignment.departure_time >= start_time, GateAssignment.arrival_time <= end_time)
            )
        ).first()

        if not overlapping:
            return gate.gate_id

    return None
