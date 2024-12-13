from delegated_validators_registry import DelegatedValidatorsRegistry
from custom_types import BLSPubkey, Gwei, DelegatorIndex
from validator import Validator
from delegators_registry import DelegatorsRegistry


class BeaconChainAccounting:
    delegators_registry: DelegatorsRegistry
    delegated_validators_registry: DelegatedValidatorsRegistry
    
    def __init__(self):
        self.delegated_validators_registry = DelegatedValidatorsRegistry()
        self.delegators_registry = DelegatorsRegistry()

    def delegate(self, delegator_index: DelegatorIndex, validator_id: BLSPubkey, amount: Gwei):
        validator = 1 # get it from the registry
        if(self.delegated_validators_registry.is_validator_delegated(validator.validator_id) == False):
            self.delegated_validators_registry.create_delegated_validator(validator, amount)

        self.delegated_validators_registry.process_delegation(delegator_index, validator.validator_id, amount)    

    def test_generate_test_data(self):
        print("Data generated")
        
        