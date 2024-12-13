from typing import List
from custom_types import Gwei, ValidatorIndex, BLSPubkey
from delegated_validator import DelegatedValidator

class DelegatedValidatorsRegistry:
    delegated_validators: List[DelegatedValidator]

    def __init__(self):
        self.delegated_validators = []

    def process_delegation(self, delegator_index: ValidatorIndex, validator_id: BLSPubkey, amount: Gwei):



