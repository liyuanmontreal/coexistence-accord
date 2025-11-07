import pandas as pd
from dataclasses import dataclass, field
from typing import List, Dict

@dataclass
class WorldState:
    year: int = 2025
    biodiv: float = 70.0
    economy: float = 70.0
    society: float = 70.0
    climate: float = 70.0
    trust: float = 60.0
    media_bias: float = 0.0
    history: List[Dict] = field(default_factory=list)

    def clamp(self):
        for k in ["biodiv", "economy", "society", "climate", "trust"]:
            v = getattr(self, k)
            setattr(self, k, max(0.0, min(100.0, v)))

    def snapshot(self):
        return {
            "year": self.year,
            "biodiv": self.biodiv,
            "economy": self.economy,
            "society": self.society,
            "climate": self.climate,
            "trust": self.trust,
            "media_bias": self.media_bias,
        }

    def record(self):
        self.history.append(self.snapshot())

    def global_metrics(self):
        return {
            "Biodiversity": self.biodiv,
            "Economy": self.economy,
            "Society": self.society,
            "Climate Stability": self.climate,
            "Trust": self.trust,
        }

    def history_df(self):
        if not self.history:
            return pd.DataFrame()
        return pd.DataFrame(self.history)

state = WorldState()
