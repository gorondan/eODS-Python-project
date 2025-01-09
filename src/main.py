"""
eODS
"""

from eods.beacon_chain_accounting import BeaconChainAccounting
from simulator import Simulator
from simulation_constants import num_ticks
from tester import Tester
from eods import *
from protocol import *

class Main:
    beacon_chain_accounting = BeaconChainAccounting()

    simulator = Simulator(beacon_chain_accounting)
    simulator.initialize_required_data()

    for _ in range(num_ticks):
        simulator.tick_delegation()
        simulator.process_rewards_penalties()
        simulator.tick_withdrawals()

    tester = Tester(beacon_chain_accounting)
    assert tester.test_quotas_sum_to_be_1()
    assert tester.test_delegated_amount_is_positive()

run = Main()

print("")