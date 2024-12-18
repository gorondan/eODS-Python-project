from beacon_chain_accounting import BeaconChainAccounting
from simulator import Simulator
from simulation_constants import num_ticks

beacon_chain_accounting = BeaconChainAccounting()

simulator = Simulator(beacon_chain_accounting)
simulator.initialize_required_data()

for _ in range(num_ticks):
    simulator.tick_delegation()
    simulator.process_rewards_penalties()
    simulator.tick_withdrawals()

print("")