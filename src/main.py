from beacon_chain_accounting import BeaconChainAccounting
from simulator import Simulator
from simulation_constants import num_ticks

beacon_chain_accounting = BeaconChainAccounting()


simulator = Simulator(beacon_chain_accounting)
simulator.initialize_required_data()

for _ in range(num_ticks):
    simulator.tick_delegation()

beacon_chain_accounting.test_generate_test_data()

beacon_chain_accounting.delegate(0, "91dbb8e1a2ff5e8822ed820f5ea8b8a3cb62436d82c3f4fa32ab5805a8b9bc53fb563d8ab387624b2e4f170b84bd2fb9", 10)