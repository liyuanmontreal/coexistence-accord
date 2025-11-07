import numpy as np

def ecological_update(state):
    S = state.biodiv / 100
    H = state.economy / 100

    r = 0.12
    K = 1.0
    alpha = 0.25
    eps = np.random.normal(0, 0.01)

    dS = r * S * (1 - S/K) - alpha * H * S + eps
    S_new = np.clip(S + dS, 0, 1)
    state.biodiv = S_new * 100
