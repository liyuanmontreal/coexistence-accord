import numpy as np

def step_ecology(state, dt=1.0):
    S = state.biodiv / 100.0
    E = state.economy / 100.0
    C = state.climate / 100.0

    r = 0.12
    K = 1.0
    alpha = 0.18
    beta = 0.22
    noise = np.random.normal(0, 0.01)

    dS = r * S * (1 - S / K) - alpha * max(0, E - 0.6) * S - beta * max(0, 0.7 - C) + noise
    S_new = float(np.clip(S + dS * dt, 0, 1))
    state.biodiv = S_new * 100.0
