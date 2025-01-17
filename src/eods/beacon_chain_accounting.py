"""
This module modifies the state of the beacon chain accounting protocol gadget.
"""
from protocol.validators_registry import ValidatorsRegistry
from eods.delegated_validators_registry import DelegatedValidatorsRegistry
from eods.delegators_registry import DelegatorsRegistry
from eods.custom_types import BLSPubkey, Gwei, DelegatorIndex

class BeaconChainAccounting:
    """
    This class is responsible for exposing the balance sheet operations - deposit, delegation and withdrawal.
    
    These are the different contexts of depositing/withdrawing:
        deposit_to_delegate_contract -> delegator balance : deposit_to_delegator_balance
        ExecutionAddress <- delegator balance : withdraw_from_delegator_balance
        delegator balance -> validator : delegate_to_validator
        delegator balance <- validator : withdraw_from_validator
    """
    
    delegators_registry: DelegatorsRegistry
    validators_registry: ValidatorsRegistry
    delegated_validators_registry: DelegatedValidatorsRegistry

    def __init__(self):
        self.delegators_registry = DelegatorsRegistry()
        self.validators_registry = ValidatorsRegistry()
        self.delegated_validators_registry = DelegatedValidatorsRegistry()

    def deposit_to_delegator_balance(self, pubkey: BLSPubkey, amount: Gwei):
        """
        This method will deposit an amount to a delegator's balance.
        If there is no delegator the registry will create one.
        """
        self.delegators_registry.deposit(pubkey, amount)
         
    def withdraw_from_delegator_balance(self, pubkey: BLSPubkey, amount: Gwei):
        """
        This method facilitates withdrawal from a delegator's balance.
        """
        self.delegators_registry.withdraw(pubkey, amount)

    def delegate_to_validator(self, delegator_index: DelegatorIndex, validator_pubkey: BLSPubkey, amount: Gwei):
        """
        This method acts as an entrypoint for delegation. It creates a delegated validator if needed and 
        it funds it with a given amount.
        
        Args:
            delegator_index (DelegatorIndex): The index of the delegator.
            validator_pubkey (BLSPubkey): The public key of the validator.
            amount (Gwei): The amount delegated.
        """
        
        validator = self.validators_registry.get_validator_by_id(validator_pubkey)

        if not self.delegated_validators_registry.is_validator_delegated(validator.pubkey):
            self.delegated_validators_registry.create_delegated_validator(validator, amount)

        self.delegated_validators_registry.process_delegation(delegator_index, validator.pubkey, amount)

    def withdraw_from_validator(self, delegator_index: DelegatorIndex, validator_pubkey: BLSPubkey, amount: Gwei):
        """
        This method acts as an entrypoint for withdrawal. 
        Args:
            delegator_index (DelegatorIndex): The index of the delegator.
            validator_pubkey (BLSPubkey): The public key of the validator.
            amount (Gwei): The amount that whould be withdrawn.
        """
        
        validator = self.validators_registry.get_validator_by_id(validator_pubkey)

        if amount < 0:
            raise ValueError("Withdrawal amount must be positive")

        if not self.delegated_validators_registry.is_validator_delegated(validator.pubkey):
            raise ValueError("Validator with the provided pubkey is not delegated validator")

        withdrawal_amount = self.delegated_validators_registry.process_withdrawal(delegator_index, validator.pubkey, amount)

        self.delegators_registry.withdraw(delegator_index, withdrawal_amount)
