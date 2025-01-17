"""
This project is designed to test, validate, and refine the foundational concepts 
that will serve as the cornerstone for eODS.
"""

from eods.beacon_chain_accounting import BeaconChainAccounting
from simulator import Simulator
from simulation_constants import num_ticks
from tester import Tester
from eods import *
from protocol import *

"""
This project provides a minimal implementation of the core eODS concepts, including a 
simulation of delegation workflows—such as depositing, delegating, withdrawing, and updating 
the balances and quotas of delegators after applying rewards, penalties or slashing. Additionally, 
it includes mechanisms to validate the integrity and consistency of the generated data.

To address these requirements, a Simulator and a Tester were developed.

The Simulator operates in discrete 'ticks' over a defined number of iterations. During each tick, it generates new delegations, applies rewards, penalties, and slashings, and processes withdrawals.

The Tester evaluates the generated data to ensure its consistency and correctness.
"""
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
