from typing import List
from custom_types import Gwei, BLSPubkey
from validator import Validator

class ValidatorsRegistry:
    validators: List[Validator]  # Stores existing validators' data as a list of Delegator instances.
    validators_balances: List[Gwei]  # List of Gwei existing validators' balances

    def __init__(self):
        # Validators lists initialization
        self.validators = []     
        self.validators_balances = [] # Max size: VALIDATOR_REGISTRY_LIMIT

    def get_validator_balance_by_id(self, pubkey : BLSPubkey):
        """Helper function to find a validator's (existing) active balance by its ID."""
        validator_index = -1

        for index, validator in enumerate(self.validators):
            if validator.pubkey == pubkey:
                validator_index = index
                break
    
        if validator_index == -1:
            raise ValueError("Validator with the given validator ID is not in validators list")
        
        return self.validators_balances[validator_index]  
        
    def get_validator_by_id(self, pubkey : BLSPubkey):
        """Helper function to find an existing validator by its ID."""
        validator = Validator()
        
        for v in self.validators:
            if v.pubkey == pubkey:
                validator = v
                break
        
        return validator