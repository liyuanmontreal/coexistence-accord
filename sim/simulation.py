from sim.ecology import step_ecology
from sim.sociology import step_sociology
from sim.coupling import step_coupling

def step_simulation(state, dt: float = 1.0):
    step_ecology(state, dt)
    step_coupling(state, dt)
    step_sociology(state, dt)
