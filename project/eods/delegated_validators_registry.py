"""
This module modifies the state of the delegated validators registry.
"""
from typing import List
from protocol.validator import Validator
from eods.custom_types import Gwei, DelegatorIndex, BLSPubkey
from eods.delegated_validator import DelegatedValidator

class DelegatedValidatorsRegistry:
    """
    This class defines the registry used to manage the delegated validators.
    """
    delegated_validators: List[DelegatedValidator]

    def __init__(self):
        self.delegated_validators = []

    def create_delegated_validator(self, validator: Validator, initial_balance: Gwei):
        """
        This method creates a new delegated validator.
        
        Args:
            validator (Validator): The validator for which a new delegated validator is created.
            initial_balance (Gwei): The initial balance of the new delegated validator.
        """
        delegated_validator = DelegatedValidator(validator, initial_balance)
        self.delegated_validators.append(delegated_validator)
        validator.delegated = True

    def is_validator_delegated(self, pubkey: BLSPubkey):
        """
        This method checks if a delegated validator with a specific pubkey exists.
        """
        is_delegated = False
        for dv in self.delegated_validators:
            if dv.delegated_validator.pubkey == pubkey:
                is_delegated = True
                break

        return is_delegated

    def process_delegation(self, delegator_index: DelegatorIndex, pubkey: BLSPubkey, amount: Gwei):
        """
        This method uses the delegated validator to process a delegation.
        """
        delegated_validator = self._get_delegated_validator_by_id(pubkey)
        delegated_validator.process_delegation(delegator_index, amount)

    def process_withdrawal(self, delegator_index: DelegatorIndex, pubkey: BLSPubkey, amount: Gwei) -> Gwei:
        """
        This method uses the delegated validator to process a withdrawal.
        """
        delegated_validator = self._get_delegated_validator_by_id(pubkey)
        
        return delegated_validator.process_withdrawal(delegator_index, amount)


    def process_rewards_penalties(self):
        """
        This method uses the delegated validator to process the rewards and penalties.
        """
        for delegated_validator in self.delegated_validators:
            delegated_validator.process_rewards_penalties()
      
    def _get_delegated_validator_by_id(self, pubkey: BLSPubkey):
        delegated_validator = None
        for dv in self.delegated_validators:
            if dv.delegated_validator.pubkey == pubkey:
                delegated_validator = dv
                break
        return delegated_validator
    