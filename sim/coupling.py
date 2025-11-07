import numpy as np

def step_coupling(state, dt=1.0):
    B = state.biodiv / 100.0
    C = state.climate / 100.0
    E = state.economy / 100.0

    emissions = max(0.0, E - 0.5)
    buffer = 0.3 * B
    dC = -0.15 * emissions + 0.12 * buffer
    C_new = float(np.clip(C + dC * dt, 0, 1))
    state.climate = C_new * 100.0

    risk_penalty = max(0.0, 0.6 - C_new)
    growth = 0.04 - 0.08 * risk_penalty
    E_new = float(np.clip(E * (1 + growth * dt), 0, 1))
    state.economy = E_new * 100.0
