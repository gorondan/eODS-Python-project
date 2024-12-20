from eods import delegated_validators_registry
from eods.delegated_validators_registry import DelegatedValidatorsRegistry
from eods.custom_types import BLSPubkey, Gwei, DelegatorIndex
from eods.delegators_registry import DelegatorsRegistry
from protocol.validators_registry import ValidatorsRegistry

class BeaconChainAccounting:
    delegators_registry: DelegatorsRegistry
    validators_registry: ValidatorsRegistry

    delegated_validators_registry: DelegatedValidatorsRegistry
    
    def __init__(self):
        self.delegated_validators_registry = DelegatedValidatorsRegistry()
        self.delegators_registry = DelegatorsRegistry()
        self.validators_registry = ValidatorsRegistry()

    def delegate(self, delegator_index: DelegatorIndex, validator_pubkey: BLSPubkey, amount: Gwei):
        validator = self.validators_registry.get_validator_by_id(validator_pubkey)

        if self.delegated_validators_registry.is_validator_delegated(validator.pubkey) == False:
            self.delegated_validators_registry.create_delegated_validator(validator, amount)
   
        self.delegated_validators_registry.process_delegation(delegator_index, validator.pubkey, amount)

    def withdraw(self, delegator_index: DelegatorIndex, validator_pubkey: BLSPubkey, amount: Gwei):
        validator = self.validators_registry.get_validator_by_id(validator_pubkey)

        if amount < 0:
            raise ValueError("Withdrawal amount must be positive")
        
        if self.delegated_validators_registry.is_validator_delegated(validator.pubkey) == False:
            raise ValueError("Validator with the provided pubkey is not delegated validator")

        self.delegated_validators_registry.process_withdrawal(delegator_index, validator.pubkey, amount) 

    def test_generate_test_data(self):
        print("Data generated")