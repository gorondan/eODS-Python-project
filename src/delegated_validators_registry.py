from typing import List
from custom_types import Gwei, ValidatorIndex, BLSPubkey
from delegated_validator import DelegatedValidator

class DelegatedValidatorsRegistry:
    delegated_validators: List[DelegatedValidator]

    def __init__(self):
        self.delegated_validators = []

    def process_delegation(self, delegator_index: ValidatorIndex, validator_id: BLSPubkey, amount: Gwei):
        delegated_validator = self._get_delegated_validator_by_id(validator_id)
        delegated_validator.increase_balance(delegator_index, amount)
        
    def _get_delegated_validator_by_id(self, validator_id: BLSPubkey):
        delegated_validator = None
        for dv in self.delegated_validators:
            if dv.delegated_validator.validator_id == validator_id:
                delegated_validator = dv
                break
        return delegated_validator
    

