from datetime import datetime, timedelta
from sqlalchemy import or_, and_
from models import Gate, GateAssignment, db

def find_available_gate(arrival_time, departure_time, buffer_minutes=30):
    """
    Find a gate ensuring no conflicts within buffer time.
    
    Args:
        arrival_time (time): Proposed arrival time
        departure_time (time): Proposed departure time
        buffer_minutes (int): Minimum minutes between assignments
    
    Returns:
        int or None: Available gate ID or None if no gate found
    """
    gates = Gate.query.all()
    arrival_datetime = datetime.combine(datetime.today(), arrival_time)
    departure_datetime = datetime.combine(datetime.today(), departure_time)

    for gate in gates:
        # Check for any assignments conflicting within buffer time
        conflicts = GateAssignment.query.filter(
            GateAssignment.gate_id == gate.gate_id,
            or_(
                # New arrival within existing assignment + buffer
                and_(
                    GateAssignment.arrival_time - timedelta(minutes=buffer_minutes) < arrival_datetime,
                    GateAssignment.departure_time + timedelta(minutes=buffer_minutes) > arrival_datetime
                ),
                # New departure within existing assignment + buffer
                and_(
                    GateAssignment.arrival_time - timedelta(minutes=buffer_minutes) < departure_datetime,
                    GateAssignment.departure_time + timedelta(minutes=buffer_minutes) > departure_datetime
                )
            )
        ).first()

        # If no conflicts found, return the gate
        if not conflicts:
            return gate.gate_id

    # No available gates found
    return None