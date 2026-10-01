"""Node seam: booking node delegates graph call to booking agent stub."""


from concierge.agents.booking_agent import BookingAgent
from concierge.nodes.error_handling import build_node_error_update
from concierge.state import ConciergeState, StateUpdate
from concierge.trace import trace


def booking_node(state: ConciergeState) -> StateUpdate:
    trace("booking_agent", turn_id=state.get("turn_id"), status="start")
    try:
        return BookingAgent().run(state)
    except Exception as exc:
        return build_node_error_update(exc)
