from core.event_engine import draw_event
from core.effect_resolver import resolve_effect
from core.state_store import state
from sim.simulation import step_simulation

class TurnManager:
    def __init__(self):
        self.current = draw_event()

    def current_event(self):
        return self.current

    def apply_choice(self, choice):
        effects = resolve_effect(choice)
        state.apply(effects)
        step_simulation(state)
        self.current = draw_event()
