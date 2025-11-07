from core.event_engine import draw_event
from core.effect_resolver import resolve_effect
from core.state_store import state
from sim.simulation import step_simulation

class TurnManager:
    def __init__(self):
        if not state.history:
            state.record()
        self.current = draw_event()

    def current_event(self):
        return self.current

    def apply_choice(self, effects: dict, media_bias: float = 0.0):
        eff = resolve_effect({"effects": effects})

        state.biodiv += eff.get("biodiv", 0)
        state.economy += eff.get("economy", 0)
        state.society += eff.get("society", 0)
        state.climate += eff.get("climate", 0)
        state.trust += eff.get("trust", 0)
        state.media_bias = media_bias
        state.clamp()

        step_simulation(state)
        state.year += 1
        state.clamp()
        state.record()

        self.current = draw_event()
