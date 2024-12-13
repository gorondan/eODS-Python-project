from delegated_validators_registry import DelegatedValidatorsRegistry
from custom_types import BLSPubkey, Gwei, DelegatorIndex
from validator import Validator
from delegators_registry import DelegatorsRegistry
from validators_registry import ValidatorsRegistry


class BeaconChainAccounting:
    delegators_registry: DelegatorsRegistry
    validators_registry: ValidatorsRegistry

    delegated_validators_registry: DelegatedValidatorsRegistry
    
    def __init__(self):
        self.delegated_validators_registry = DelegatedValidatorsRegistry()
        self.delegators_registry = DelegatorsRegistry()
        self.validators_registry = ValidatorsRegistry()

    def delegate(self, delegator_index: DelegatorIndex, validator_id: BLSPubkey, amount: Gwei):
        validator = self.validators_registry.get_validator_by_id(validator_id)
        
        if(self.delegated_validators_registry.is_validator_delegated(validator.validator_id) == False):
            self.delegated_validators_registry.create_delegated_validator(validator, amount)

        self.delegated_validators_registry.process_delegation(delegator_index, validator.validator_id, amount)    

    def test_generate_test_data(self):
        print("Data generated")
        
        