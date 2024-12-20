from typing import List
from validator import Validator
from custom_types import Gwei, DelegatorIndex, BLSPubkey
from delegated_validator import DelegatedValidator

class DelegatedValidatorsRegistry:
    delegated_validators: List[DelegatedValidator]

    def __init__(self):
        self.delegated_validators = []

    def process_delegation(self, delegator_index: DelegatorIndex, pubkey: BLSPubkey, amount: Gwei):
        delegated_validator = self._get_delegated_validator_by_id(pubkey)
        delegated_validator.increase_balance(delegator_index, amount)

    def process_withdrawal(self, delegator_index: DelegatorIndex, pubkey: BLSPubkey, amount: Gwei):
        delegated_validator = self._get_delegated_validator_by_id(pubkey)
        delegated_validator.decrease_balance(delegator_index, amount)

    def create_delegated_validator(self, validator: Validator, initial_balance: Gwei):
        delegated_validator = DelegatedValidator(validator, initial_balance)
        self.delegated_validators.append(delegated_validator)
        validator.delegated = True

    def is_validator_delegated(self, pubkey: BLSPubkey):
        is_delegated = False
        for dv in self.delegated_validators:
            if dv.delegated_validator.pubkey == pubkey:
                is_delegated = True
                break

        return is_delegated
     
    def process_rewards_penalties(self):
        for delegated_validator in self.delegated_validators:
            delegated_validator.process_rewards_penalties()
        
    def _get_delegated_validator_by_id(self, pubkey: BLSPubkey):
        delegated_validator = None
        for dv in self.delegated_validators:
            if dv.delegated_validator.pubkey == pubkey:
                delegated_validator = dv
                break
        return delegated_validator
    

