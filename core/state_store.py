import pandas as pd

class State:
    def __init__(self):
        self.year = 2025
        self.biodiv = 70
        self.economy = 70
        self.society = 70
        self.climate = 70
        self.history = []

    def apply(self, effects):
        self.biodiv += effects["biodiv"]
        self.economy += effects["economy"]
        self.society += effects["society"]
        self.climate += effects["climate"]
        self.year += 1

        for attr in ["biodiv","economy","society","climate"]:
            v = getattr(self, attr)
            setattr(self, attr, max(0, min(100, v)))

        self.history.append([self.year,self.biodiv,self.economy,self.society,self.climate])

    def global_metrics(self):
        return {
            "Biodiversity": self.biodiv,
            "Economy": self.economy,
            "Society": self.society,
            "Climate Stability": self.climate
        }

    def history_df(self):
        if not self.history:
            return pd.DataFrame()
        return pd.DataFrame(self.history, columns=["year","biodiv","economy","society","climate"])

state = State()
