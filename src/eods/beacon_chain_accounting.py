"""
This module defines a model for beacon-chain accounting, to accomodates delegators in Ethereum
"""
from protocol.validators_registry import ValidatorsRegistry
from eods.delegated_validators_registry import DelegatedValidatorsRegistry
from eods.delegators_registry import DelegatorsRegistry
from eods.custom_types import BLSPubkey, Gwei, DelegatorIndex

class BeaconChainAccounting:
    """
    The following are the methods that modify the state of beacon-chain accounting
    """
    delegators_registry: DelegatorsRegistry
    validators_registry: ValidatorsRegistry

    delegated_validators_registry: DelegatedValidatorsRegistry

    def __init__(self):
        self.delegated_validators_registry = DelegatedValidatorsRegistry()
        self.delegators_registry = DelegatorsRegistry()
        self.validators_registry = ValidatorsRegistry()

    def delegate(self, delegator_index: DelegatorIndex, validator_pubkey: BLSPubkey, amount: Gwei):
        validator = self.validators_registry.get_validator_by_id(validator_pubkey)

        if not self.delegated_validators_registry.is_validator_delegated(validator.pubkey):
            self.delegated_validators_registry.create_delegated_validator(validator, amount)

        self.delegated_validators_registry.process_delegation(delegator_index, validator.pubkey, amount)

    def withdraw(self, delegator_index: DelegatorIndex, validator_pubkey: BLSPubkey, amount: Gwei):
        validator = self.validators_registry.get_validator_by_id(validator_pubkey)

        if amount < 0:
            raise ValueError("Withdrawal amount must be positive")

        if not self.delegated_validators_registry.is_validator_delegated(validator.pubkey):
            raise ValueError("Validator with the provided pubkey is not delegated validator")

        self.delegated_validators_registry.process_withdrawal(delegator_index, validator.pubkey, amount)
    
    def test_generate_test_data(self):
        print("Data generated")
