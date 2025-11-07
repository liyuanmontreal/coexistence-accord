def step_sociology(state, dt=1.0):
    T = state.trust / 100.0
    E = state.economy / 100.0
    B = state.biodiv / 100.0
    M = state.media_bias

    media_effect = -0.25 * M
    desired = 0.4 * E + 0.3 * B + 0.3
    dT = 0.6 * (desired - T) + media_effect
    T_new = max(0.0, min(1.0, T + dT * dt))
    state.trust = T_new * 100.0

    state.society = max(0.0, min(100.0, 0.6 * state.society + 0.4 * state.trust))
