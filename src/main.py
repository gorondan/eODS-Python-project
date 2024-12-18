from beacon_chain_accounting import BeaconChainAccounting
from simulator import Simulator

beacon_chain_accounting = BeaconChainAccounting()


simulator = Simulator()
simulator.initialize_required_data(
    beacon_chain_accounting.validators_registry, 
    beacon_chain_accounting.delegators_registry
    )



beacon_chain_accounting.test_generate_test_data()

beacon_chain_accounting.delegate(0, "91dbb8e1a2ff5e8822ed820f5ea8b8a3cb62436d82c3f4fa32ab5805a8b9bc53fb563d8ab387624b2e4f170b84bd2fb9", 10)